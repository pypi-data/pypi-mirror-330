from numpy import copy, eye, triu, zeros, gcd


def forwardsub(L,b):
	"""
 	forwardsub(L,b)

	Solve the lower-triangular linear system with matrix L and right-hand side
	vector b.
	"""
	n = len(b)
	x = zeros(n)
	for i in range(n):
		s = L[i,:i] @ x[:i]
		x[i] = ( b[i] - s ) / L[i,i]
	return x


def backsub(U,b):
	"""
	backsub(U,b)

	Solve the upper-triangular linear system with matrix U and right-hand side
	vector b.
	"""
	n = len(b)
	x = zeros(n)
	for i in range(n-1,-1,-1):
		s = U[i,i+1:] @ x[i+1:]
		x[i] = ( b[i] - s ) / U[i,i]
	return x

def lufact(A):
	"""
	lufact(A)

	Compute the LU factorization of square matrix A, returning the factors.
	"""
	n = A.shape[0]
	L = eye(n)      # puts ones on diagonal
	U = copy(A)

	# Gaussian elimination
	for j in range(n-1):
		for i in range(j+1,n):
			L[i,j] = U[i,j] / U[j,j]   # row multiplier
			U[i,j:] = U[i,j:] - L[i,j]*U[j,j:]
	return L,triu(U)

def _lufact2(A):
	"""
	lufact(A)

	Compute the LU factorization of square matrix A, returning the factors.
	"""
	n = A.shape[0]
	L = eye(n, dtype=A.dtype)  # puts ones on diagonal
	U = copy(A)
	D = eye(n, dtype=A.dtype)

	# Gaussian elimination
	for j in range(n-1):
		L[j,j] = U[j,j]  # diagonal of L, scaled by U[j,j]
		for i in range(j+1,n):
			L[i,j] = U[i,j]   # row multiplier, scaled by U[j,j]
			U[i] = U[i]*U[j,j] - L[i,j]*U[j] # row operation, each term scaled by U[j,j]
		D[j,j] = U[j,j] # record scaling factors
	# Now each column of L is scaled by the corresponding diagonal of U
	# and each row of U is scaled by the running product of the previous diagonals of D
	# That is,
	# realL @ realU = A
	# L = realL @ D
	# U = D @ realU
	# It is impossible to solve in general LU = D'A by this method, so it is not useful
	return L,triu(U), D

def lufactint(A):
	"""
	lufactint(A)

	Compute the LU factorization of square matrix A using integer arithmetic,
	returning the factors such that L @ U = diag(d) @ A.
	"""
	n = A.shape[0]
	L = eye(n, dtype=A.dtype)  # puts ones on diagonal
	U = copy(A)
	d = zeros(n, dtype=A.dtype)
	# Gaussian elimination
	for j in range(n-1):
		rowscale = U[j,j]
		for i in range(j+1,n):
			# Try to find a smaller row scale to minimize the risk of overflow
			# This is not necessary, but it helps to avoid overflow in some cases
			thiscol_ldiv = gcd(rowscale, U[i,j])
			thiscol_rowscale = rowscale // thiscol_ldiv
			# Like in lufact, but scaled by `thiscol_rowscale`
			L[i,j] = U[i,j] // thiscol_ldiv
			# Rescale both entire rows (instead of columns), so that they manifest as a
			# left multiplication of a diagonal matrix, as the question wants
			U[i] = U[i] * thiscol_rowscale
			L[i,:j] = L[i,:j] * thiscol_rowscale # Don't touch [i,j] cuz it's already good
			U[i] = U[i] - L[i,j] * U[j] # Like in lufact, but scaled by `rowscale`
			# Update D to reflect the rescaling
			# BEWARE of integer overflow! (NumPy will warn you if this happens)
			# This D turns out to be a running product of U[j,j] (notwithstanding the gcd trick)
			d[i] *= thiscol_rowscale
	return L, U, d
