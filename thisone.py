import streamlit as st

def is_triangular(a, b, c):
    if (a + b > c) and (b + c > a) and (c + a > b):
        return True
    else:
        return False

def main():
    st.title("Triangle Checker")
    a = st.number_input("Enter side 'a':")
    b = st.number_input("Enter side 'b':")
    c = st.number_input("Enter side 'c':")

    if st.button("Check Triangle"):
        if is_triangular(a, b, c):
            st.success("These numbers can form a triangle.")
        else:
            st.error("These numbers cannot form a triangle.")

if __name__ == "__main__":
    main()
