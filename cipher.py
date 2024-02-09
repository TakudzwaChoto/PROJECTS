import streamlit as st
import string

st.title('Shift Cipher')
st.write("""
This app takes a phrase and decodes it using a shift cipher. For instance, "A"
shifted by 1 becomes "B".

For phrases containing non-alpha characters like numbers and spaces, the non-alpha characters 
will not be transformed using the shift cipher. Those characters will appear in
result in the same position.

Cipher will preserve a character's case.
""")
st.write('---')
 
# Widgets
st.header('Inputs')
phrase = st.text_input("Phrase: ")
shift_dir = st.selectbox("Shift direction: ", ('Forward', 'Backward'))
shift_no = st.number_input("Shift Amount: ", min_value=1)

st.cache()
def create_dict():
    letter_to_no = {}
    no_to_letter = {}

    for no, letter in enumerate(string.ascii_lowercase):
        letter_to_no[letter] = no
        no_to_letter[no] = letter
    
    return letter_to_no, no_to_letter

letter_to_no, no_to_letter = create_dict()

st.cache()
def shift(phrase, shift_dir, shift_no):
    answer = ''
    
    for i in phrase:
        #Returns True if i is uppercase
        upper_case = i.isupper() 
        
        #Casts i to lowercase since dictionaries use lowercase
        i = i.lower()            
        
        if i in letter_to_no.keys():
            ind = letter_to_no[i]
            
            if shift_dir == 'Forward':
                shift_ind = ind + shift_no
            else:
                shift_ind = ind - shift_no
            
            # Divides by 26 because alphabet has 26 letters
            # Uses remainder as key
            sub = no_to_letter[shift_ind % 26]
        
        else:
            sub = i
        
        sub = sub.upper() if upper_case else sub
        answer = answer + sub
    
    return answer

answer = shift(phrase, shift_dir, shift_no)

# Outputs
st.header('⭐️ Results')
st.write(f'Decoded Phrase: {answer}')