from backSub import pivoting
def test_pivoting():
    # Test case 1: Simple row echelon form matrix
    U1 = [
        [1, 2, 0],
        [0, 0, 1],
        [0, 0, 0]
    ]
    pivot, freeVars = pivoting(U1)
    print(f"Pivot: {pivot}")
    print(f"Free Variables: {freeVars}")

    # Test case 2: Full rank matrix (identity matrix)
    U2 = [
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1]
    ]
    pivot, freeVars = pivoting(U2)
    print(f"Pivot: {pivot}")
    print(f"Free Variables: {freeVars}")

    # Test case 3: Matrix with all zeros
    U3 = [
        [0, 0],
        [0, 0]
    ]

    pivot, freeVars = pivoting(U3)
    print(f"Pivot: {pivot}")
    print(f"Free Variables: {freeVars}")

    U4 = [
        [0, 5, 2,3],
        [0, 0, 2,3],
        [0, 0,0,1],
        [0,0,0,0]
    ]
    pivot, freeVars = pivoting(U4)
    print(f"Pivot: {pivot}")
    print(f"Free Variables: {freeVars}")


test_pivoting()
