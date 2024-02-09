import streamlit as st

def is_triangular(num):
    n = 1
    triangular_num = 1
    
    while triangular_num < num:
        n += 1
        triangular_num = n * (n + 1) // 2
    
    return triangular_num == num

def main():
    st.title("Triangular Number Checker")
    
    num1 = st.text_input("Enter the first number:")
    num2 = st.text_input("Enter the second number:")
    num3 = st.text_input("Enter the third number:")
    
    if st.button("Check"):
        try:
            num1 = int(num1)
            num2 = int(num2)
            num3 = int(num3)
            
            result1 = "Triangular" if is_triangular(num1) else "Not Triangular"
            result2 = "Triangular" if is_triangular(num2) else "Not Triangular"
            result3 = "Triangular" if is_triangular(num3) else "Not Triangular"
            
            st.write(f"First Number: {result1}")
            st.write(f"Second Number: {result2}")
            st.write(f"Third Number: {result3}")
            
        except ValueError:
            st.error("Error: Invalid input. Please enter a valid number.")

if __name__ == "__main__":
    main()
