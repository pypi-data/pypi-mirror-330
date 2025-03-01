import jax
import jax.numpy as jnp
import numpy as np
import pandas as pd
from pyxtal import pyxtal
from pymatgen.core import Structure, Lattice
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer
from functools import partial
import multiprocessing
import os
import re
from slices.wyckoff import symops, mult_table
from slices.elements import element_list, sg_encoding

@jax.vmap
def sort_atoms(W, A, X):
    """
    lex sort atoms according W, X, Y, Z

    W: (n, )
    A: (n, )
    X: (n, dim) int
    """
    W_temp = jnp.where(W>0, W, 9999) # change 0 to 9999 so they remain in the end after sort

    X -= jnp.floor(X)
    idx = jnp.lexsort((X[:,2], X[:,1], X[:,0], W_temp))

    #assert jnp.allclose(W, W[idx])
    A = A[idx]
    X = X[idx]
    return A, X

def letter_to_number(letter):
    """
    'a' to 1 , 'b' to 2 , 'z' to 26, and 'A' to 27 
    """
    return ord(letter) - ord('a') + 1 if 'a' <= letter <= 'z' else 27 if letter == 'A' else None

def shuffle(key, data):
    """
    shuffle data along batch dimension
    """
    G, L, XYZ, A, W = data
    idx = jax.random.permutation(key, jnp.arange(len(L)))
    return G[idx], L[idx], XYZ[idx], A[idx], W[idx]
    
def process_one(cif, atom_types, wyck_types, n_max, tol=0.01):
    """
    # taken from https://anonymous.4open.science/r/DiffCSP-PP-8F0D/diffcsp/common/data_utils.py
    Process one cif string to get G, L, XYZ, A, W

    Args:
      cif: cif string
      atom_types: number of atom types
      wyck_types: number of wyckoff types
      n_max: maximum number of atoms in the unit cell
      tol: tolerance for pyxtal

    Returns:
      G: space group number
      L: lattice parameters
      XYZ: fractional coordinates
      A: atom types
      W: wyckoff letters
    """
    crystal = Structure.from_str(cif, fmt='cif')
    spga = SpacegroupAnalyzer(crystal, symprec=tol)
    crystal = spga.get_refined_structure()
    c = pyxtal()
    try:
        c.from_seed(crystal, tol=0.01)
    except:
        c.from_seed(crystal, tol=0.0001)
    
    g = c.group.number
    num_sites = len(c.atom_sites)
    assert (n_max > num_sites) # we will need at least one empty site for output of L params

    print (g, c.group.symbol, num_sites)
    natoms = 0
    ww = []
    aa = []
    fc = []
    ws = []
    for site in c.atom_sites:
        a = element_list.index(site.specie) 
        x = site.position
        m = site.wp.multiplicity
        w = letter_to_number(site.wp.letter)
        symbol = str(m) + site.wp.letter
        natoms += site.wp.multiplicity
        assert (a < atom_types)
        assert (w < wyck_types)
        assert (np.allclose(x, site.wp[0].operate(x)))
        aa.append( a )
        ww.append( w )
        fc.append( x )  # the generator of the orbit
        ws.append( symbol )
        print ('g, a, w, m, symbol, x:', g, a, w, m, symbol, x)
    idx = np.argsort(ww)
    ww = np.array(ww)[idx]
    aa = np.array(aa)[idx]
    fc = np.array(fc)[idx].reshape(num_sites, 3)
    ws = np.array(ws)[idx]
    print (ws, aa, ww, natoms) 

    aa = np.concatenate([aa,
                        np.full((n_max - num_sites, ), 0)],
                        axis=0)

    ww = np.concatenate([ww,
                        np.full((n_max - num_sites, ), 0)],
                        axis=0)
    fc = np.concatenate([fc, 
                         np.full((n_max - num_sites, 3), 1e10)],
                        axis=0)
    
    abc = np.array([c.lattice.a, c.lattice.b, c.lattice.c])/natoms**(1./3.)
    angles = np.array([c.lattice.alpha, c.lattice.beta, c.lattice.gamma])
    l = np.concatenate([abc, angles])
    
    print ('===================================')

    return g, l, fc, aa, ww 

def GLXYZAW_from_file(csv_file, atom_types, wyck_types, n_max, num_workers=1):
    """
    Read cif strings from csv file and convert them to G, L, XYZ, A, W
    Note that cif strings must be in the column 'cif'

    Args:
      csv_file: csv file containing cif strings
      atom_types: number of atom types
      wyck_types: number of wyckoff types
      n_max: maximum number of atoms in the unit cell
      num_workers: number of workers for multiprocessing

    Returns:
      G: space group number
      L: lattice parameters
      XYZ: fractional coordinates
      A: atom types
      W: wyckoff letters
    """
    data = pd.read_csv(csv_file)
    cif_strings = data['cif']

    p = multiprocessing.Pool(num_workers)
    partial_process_one = partial(process_one, atom_types=atom_types, wyck_types=wyck_types, n_max=n_max)
    results = p.map_async(partial_process_one, cif_strings).get()
    p.close()
    p.join()

    G, L, XYZ, A, W = zip(*results)

    G = jnp.array(G) 
    A = jnp.array(A).reshape(-1, n_max)
    W = jnp.array(W).reshape(-1, n_max)
    XYZ = jnp.array(XYZ).reshape(-1, n_max, 3)
    L = jnp.array(L).reshape(-1, 6)

    A, XYZ = sort_atoms(W, A, XYZ)
    
    return G, L, XYZ, A, W


def GLXAW_to_structure_single(G, L, XYZ, A, W, tol_empty=1e9):
    """
    逆 process_one: 将 (G, L, XYZ, A, W) 还原成 pymatgen 的 Structure 对象。

    参数：
    ----------
    G : int
        空间群号 (space group number)，取值 1~230。
    L : ndarray of shape (6,)
        经过缩放后的晶格参数 [a, b, c, alpha, beta, gamma]，
        其中 a,b,c 已被除以 (natoms^(1/3))。
    XYZ : ndarray of shape (n_max, 3)
        每个 Wyckoff "位点"生成元（分数坐标）。空位一般会被填充为 1e10 之类的占位值。
    A : ndarray of shape (n_max,)
        每个位点对应的元素编号（对照 `element_list`）。若为 0 则是空位。
    W : ndarray of shape (n_max,)
        每个位点对应的 Wyckoff letter 编码（1 表示 'a', 2 表示 'b', ... , 0 表示空位）。
    tol_empty : float
        若 XYZ[i] 的坐标远大于 1，则默认认为是空位的 padding。

    返回：
    ----------
    structure : pymatgen.core.Structure
        还原出的 pymatgen 结构对象。
    """

    # 1. 先根据 W 数组，统计总原子数 natoms
    #    注意：W[i] != 0 时，对应一个有效的 Wyckoff 生成元
    #    其对应的乘重（multiplicity）为 mult_table[G-1, W[i]]。
    natoms = 0
    n_max = len(W)
    for i in range(n_max):
        w_i = W[i]
        if w_i != 0:
            natoms += mult_table[G-1, w_i]

    # 若整个条目其实为空，直接返回一个空结构
    if natoms == 0:
        return Structure(Lattice.cubic(1.0), [], [])

    # 2. 恢复真实晶格参数 (a, b, c)
    a, b, c, alpha_rad, beta_rad, gamma_rad = L
    scale = natoms ** (1.0 / 3.0)  # 与 process_one 中的缩放相反
    a *= scale
    b *= scale
    c *= scale

    # 将角度从弧度转换为度
    alpha = np.degrees(alpha_rad)
    beta = np.degrees(beta_rad)
    gamma = np.degrees(gamma_rad)

    lattice = Lattice.from_parameters(a, b, c, alpha, beta, gamma)

    # 3. 根据每个 Wyckoff 生成元，扩展出所有原子坐标
    all_coords = []
    all_species = []
    for i in range(n_max):
        w_i = W[i]
        if w_i == 0:
            # 说明这是个空padding
            continue

        # 如果 XYZ[i] 非常大( ~1e10 )，表明是个空位
        if np.any(np.abs(XYZ[i]) > tol_empty):
            continue

        # 元素符号
        a_i = A[i]  # 元素编号
        if a_i == 0:
            # 空位，不添加原子
            continue
        try:
            element_symbol = element_list[a_i]
        except IndexError:
            raise ValueError(f"元素编号 {a_i} 超出 `element_list` 的范围。")

        # 该 Wyckoff 位点的 multiplicity
        m = mult_table[G-1, w_i].item()  # 注意可能是 jax.numpy 类型，需要 item() -> int

        # 取出对应的对称操作
        # symops[g-1, w, :m] 的形状是 (m, 3, 4)
        ops = symops[G-1, w_i, :m]

        # 将分数坐标拼成仿射坐标 [x, y, z, 1]
        frac_coord = np.array([XYZ[i, 0], XYZ[i, 1], XYZ[i, 2], 1.0])

        # 对称扩展
        expanded_coords = ops @ frac_coord.T  # 得到 shape (m, 3)
        # 将坐标约束到 [0,1) 范围
        expanded_coords = expanded_coords % 1.0

        # 逐个原子塞进 list
        for j in range(m):
            all_coords.append(expanded_coords[j])
            all_species.append(element_symbol)

    # 4. 构造 pymatgen 的 Structure 对象
    structure = Structure(
        lattice,
        species=all_species,
        coords=all_coords,
        coords_are_cartesian=False
    )

    return structure


def GLXA_to_csv(G, L, X, A, num_worker=1, filename='out_structure.csv'):

    L = np.array(L)
    X = np.array(X)
    A = np.array(A)
    p = multiprocessing.Pool(num_worker)
    if isinstance(G, int):
        G = np.array([G] * len(L))
    structures = p.starmap_async(GLXA_to_structure_single, zip(G, L, X, A)).get()
    p.close()
    p.join()

    data = pd.DataFrame()
    data['cif'] = structures
    header = False if os.path.exists(filename) else True
    data.to_csv(filename, mode='a', index=False, header=header)


def tokenize_enc(enc_string):
    """
    Tokenizes the 'enc' string based on the following rules:
    - First digit: 0->o, 1->+
    - Second digit: 0->z, 1->y, 2->x, etc.
    - Last digit if it's 0: 0->o
    - If fourth from last is 1: 1->+
    - Three consecutive uppercase letters or three consecutive digits are treated as one token
    - Existing lowercase letters are preserved
    
    Args:
        enc_string (str): The 'enc' string to tokenize.
    
    Returns:
        str: The tokenized string with tokens separated by spaces.
    """
    # Convert string to list for easier manipulation
    chars = list(enc_string)
    
    # Handle first digit (0->o, 1->+)
    if chars[0] == '0':
        chars[0] = 'o'
    elif chars[0] == '1':
        chars[0] = '+'
    
    # Handle second digit (0->z, 1->y, etc) only if it's a digit
    if len(chars) > 1 and chars[1].isdigit():
        chars[1] = chr(ord('z') - int(chars[1]))
    
    # Handle last digit if it's 0
    if chars[-1] == '0':
        chars[-1] = 'o'
    
    # Handle fourth from last if it's 1
    if len(chars) >= 4 and chars[-4] == '1':
        chars[-4] = '+'
    
    # Join back to string
    converted_string = ''.join(chars)
    
    # Regular expression to match three uppercase letters or three consecutive digits
    pattern = re.compile(r'[A-Z]{3}|.')
    
    tokens = pattern.findall(converted_string)
    
    # Filter out any empty strings (if any)
    tokens = [token for token in tokens if token]
    
    # Join tokens with space
    tokenized = ' '.join(tokens)
    
    return tokenized

def get_tokenized_enc(int_number):
    """
    Given an int_number, finds the corresponding 'enc' string in sg_encoding,
    tokenizes it, and returns the tokenized version.
    
    Args:
        int_number (int): The integer number to search for.
    
    Returns:
        str: The tokenized 'enc' string.
    
    Raises:
        ValueError: If the int_number is not found in sg_encoding.
    """
    for symbol, properties in sg_encoding.items():
        if properties.get('int_number') == int_number:
            enc_string = properties.get('enc')
            tokenized = tokenize_enc(enc_string)
            return tokenized
    raise ValueError(f"int_number {int_number} not found in sg_encoding.")
    
def get_space_group_num(enc):
    """
    Given an 'enc' string, finds the corresponding 'int_number' in sg_encoding.

    Args:
        enc (str): The 'enc' string to search for.

    Returns:
        int: The corresponding 'int_number'.

    Raises:
        ValueError: If the 'enc' string is not found in sg_encoding.
    """
    for symbol, properties in sg_encoding.items():
        if properties.get('enc') == enc:
            int_number = properties.get('int_number')
            return int_number
    raise ValueError(f"enc {enc} not found in sg_encoding.")

def get_space_group_num_from_letter_enc(letter_enc):
    """
    Given a letter encoded string, converts it back to number encoding and returns the space group number.
    Reverse mapping:
    - First letter: o->0, +->1
    - Second letter: z->0, y->1, x->2, etc.
    - Last letter if o: o->0
    - Fourth from last if +: +->1
    
    Args:
        letter_enc (str): The letter encoded string without spaces.
    
    Returns:
        int: The corresponding space group number.
    
    Raises:
        ValueError: If the encoding is not found in sg_encoding.
    """
    # Convert string to list for easier manipulation
    chars = list(letter_enc)
    
    # Handle first letter
    if chars[0] == 'o':
        chars[0] = '0'
    elif chars[0] == '+':
        chars[0] = '1'
    
    # Handle second letter
    if len(chars) > 1 and chars[1].islower():
        chars[1] = str(ord('z') - ord(chars[1]))
    
    # Handle last letter if it's o
    if chars[-1] == 'o':
        chars[-1] = '0'
    
    # Handle fourth from last if it's +
    if len(chars) >= 4 and chars[-4] == '+':
        chars[-4] = '1'
    
    number_enc = ''.join(chars)
    return get_space_group_num(number_enc)

# Example Usage
if __name__ == "__main__":
    # Example int_number
    example_int_number = 41  # Corresponds to 'Aba2' with enc '03aODDbOOOjDDO0'
    
    try:
        tokenized_enc = get_tokenized_enc(example_int_number)
        print(f"Tokenized 'enc' for int_number {example_int_number}:")
        print(tokenized_enc)
        
        # Test the new function
        letter_enc = ''.join(tokenized_enc.split())  # Remove spaces
        print(f"Space group number from letter encoded string '{letter_enc}':")
        print(get_space_group_num_from_letter_enc(letter_enc))
    except ValueError as e:
        print(e)

if __name__=='__main__':
    atom_types = 119
    wyck_types = 28
    n_max = 24

    import numpy as np 
    np.set_printoptions(threshold=np.inf)
    
    #csv_file = '../data/mini.csv'
    #csv_file = '/home/wanglei/cdvae/data/carbon_24/val.csv'
    #csv_file = '/home/wanglei/cdvae/data/perov_5/val.csv'
    csv_file = '/home/wanglei/cdvae/data/mp_20/train.csv'

    G, L, XYZ, A, W = GLXYZAW_from_file(csv_file, atom_types, wyck_types, n_max)
    
    print (G.shape)
    print (L.shape)
    print (XYZ.shape)
    print (A.shape)
    print (W.shape)
    
    print ('L:\n',L)
    print ('XYZ:\n',XYZ)


    @jax.vmap
    def lookup(G, W):
        return mult_table[G-1, W] # (n_max, )
    M = lookup(G, W) # (batchsize, n_max)
    print ('N:\n', M.sum(axis=-1))
