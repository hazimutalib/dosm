import streamlit as st

st.write(""" # Postage Calculator """)


sender = st.selectbox("From:",['West Malaysia','Sarawak', 'Sabah'])
receiver = st.selectbox("To:",['West Malaysia','Sarawak', 'Sabah'])
weight = st.selectbox("Weight (kg):",['<0.5','<1.0','<1.5','<2.0','<2.5','<3.0'])

st.write(""" # Courier """)
courier = st.selectbox("Choose courier service:", [
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

st.write("""### Rates: RM {}""".format(rate))
