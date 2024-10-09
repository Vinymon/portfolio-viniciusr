import streamlit as st

def app():
    st.title('About this project.')

    st.write("This project was initiated to address the challenge of finding a system compatible with our production flow. The company's sales rely on supplier stock, but we do not engage in dropshipping. It was also crucial that the system supports the financial health of the company. Therefore, we developed a simplified system to minimize costs, with customization options as needed. The comprehensive system includes all production stages, from purchasing to product production and cost/sales reporting. We previously struggled with information organization and expense tracking, leading to losses and difficulties in setting growth targets and managing cash flow. In my portfolio, I offer an overview of the system for easier understanding. It's worth noting that the entire system is hosted on an Amazon AWS EC2 instance. I am available to answer any questions.")
    st.write("And to illustrate the project's functionality, I've entered some fictional data, which represent products in the company's production line. In the sidebar, there's a 'Reset Data' button, which, when clicked, resets the test data to its original state.")

    st.subheader('Other Projects')
    st.write('')
    st.write('I developed an automatic proposal generation system in PPTx format, integrated with the CRM used by the sales team. This system customizes proposals by including images of the product in the color selected by the customer, optimizing the sales process and providing a personalized experience.')
    video_file = open('Streamlit Video.mp4', 'rb')

    # Anexar o vídeo no app
    st.video(video_file.read(), format='video/mp4')

    st.write("As demonstrated in the video, the proposal automation system is seamlessly integrated with the CRM. Initially, the proposal card is populated with products, their prices, and quantities. Following this, a task of the 'Proposal' type is created, alongside a proposal number - in this instance, I used 'Test'. Subsequently, the completed proposal is saved to the OneDrive page of the assigned team member. The PowerPoint proposal contains all the data that has been entered into the CRM up to that point.")
    st.write('---')
    st.write('I implemented the automation of syncing supplier inventory with our internal system through APIs. This process ensures real-time updates of our inventory, enhancing operational efficiency and the accuracy of stock control.')