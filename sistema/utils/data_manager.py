import pandas as pd

def save_proposal(seller_name, proposal_number, client_name, products):
    # Cria um DataFrame para os produtos
    df = pd.DataFrame(products)
    df['Vendedor'] = seller_name
    df['NumeroProposta'] = proposal_number
    df['Cliente'] = client_name
    
    # Concatena ou cria um novo arquivo xlsx com os dados da proposta
    try:
        existing_df = pd.read_excel("Propostas.xlsx")
        final_df = pd.concat([existing_df, df])
    except FileNotFoundError:
        final_df = df
    final_df.to_excel("Propostas.xlsx", index=False)