import streamlit as st
import base64

my_expander = st.beta_expander()
with my_expander:
    'Hello there!'
    clicked = st.button('Click me!')


def st_pdf_display(pdf_file):
	with open(pdf_file,"rb") as f:
		base64_pdf = base64.b64encode(f.read()).decode('utf-8')
	pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="700" height="700" type="application/pdf">' 
	st.markdown(pdf_display, unsafe_allow_html=True)

st_pdf_display("Test.pdf")


st.sidebar.write(""" # Postage Calculator """)
sender = st.sidebar.selectbox("From:",['West Malaysia','East Malaysia'])
receiver = st.sidebar.selectbox("To:",['West Malaysia','East Malaysia'])
weight = st.sidebar.selectbox("Weight (kg):",['<0.5','<1.0','<1.5','<2.0','<2.5','<3.0'])

st.sidebar.write(""" # Courier """)
courier = st.sidebar.selectbox("Choose courier service:", [
     'DHL', 
    'J&T', 'Poslaju'
])


if courier == 'Poslaju':
	if sender == receiver :
		if weight == '<0.5':
			rate = 6.0
		elif weight == '<1.0':
			rate = 8.6
		elif weight == '<1.5':
			rate = 11.3
		elif weight == '<2.0':
			rate = 13.9
		elif weight == '<2.5':
			rate = 21.2
		elif weight == '<3.0':
			rate = 23.9
	else:
		if weight == '<0.5':
			rate = 8.0
		elif weight == '<1.0':
			rate = 9.6
		elif weight == '<1.5':
			rate = 13.3
		elif weight == '<2.0':
			rate = 15.9
		elif weight == '<2.5':
			rate = 23.2
		elif weight == '<3.0':
			rate = 25.9

if courier == 'DHL':
	if sender == receiver :
		if weight == '<0.5':
			rate = 6.5
		elif weight == '<1.0':
			rate = 9.0
		elif weight == '<1.5':
			rate = 11.5
		elif weight == '<2.0':
			rate = 14.2
		elif weight == '<2.5':
			rate = 21.8
		elif weight == '<3.0':
			rate = 24.5
	else:
		if weight == '<0.5':
			rate = 8.5
		elif weight == '<1.0':
			rate = 9.9
		elif weight == '<1.5':
			rate = 13.8
		elif weight == '<2.0':
			rate = 16.0
		elif weight == '<2.5':
			rate = 23.0
		elif weight == '<3.0':
			rate = 26.0

if courier == 'J&T':
	if sender == receiver :
		if weight == '<0.5':
			rate = 5.0
		elif weight == '<1.0':
			rate = 6.5
		elif weight == '<1.5':
			rate = 8.0
		elif weight == '<2.0':
			rate = 9.5
		elif weight == '<2.5':
			rate = 11.0
		elif weight == '<3.0':
			rate = 12.5
	else:
		if weight == '<0.5':
			rate = 5.5
		elif weight == '<1.0':
			rate = 7.0
		elif weight == '<1.5':
			rate = 8.5
		elif weight == '<2.0':
			rate = 10.0
		elif weight == '<2.5':
			rate = 11.5
		elif weight == '<3.0':
			rate = 13.0

st.sidebar.write("""### Rates: RM {}""".format(rate))
