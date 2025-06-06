
import streamlit as st
import requests
from bs4 import BeautifulSoup

st.title("Detector de Checkout, Gateway e Formas de Pagamento")

url = st.text_input("Cole aqui o link do código-fonte do checkout (com ou sem 'view-source:')")

def analisar_checkout(html):
    html = html.lower()
    resultado = {
        'Checkout Detectado': [],
        'Gateways Detectados': [],
        'Formas de Pagamento': [],
        'Possível Associação': {}
    }

    checkouts = {
        'Appmax': ['window.appmax', 'data-appmax', 'appmax.checkout'],
        'Yampi': ['yampi.checkout', 'data-store', 'yampi-token'],
        'Cartpanda': ['panda-checkout', 'cartpanda.checkout', 'window.cartpanda'],
        'Nuvemshop': ['window.__nuvem__', 'nuvem-checkout', 'nuvemshop.cart'],
        'Shopify': ['shopify.checkout', 'shopify-features', 'cdn.shopify.com'],
        'Kiwify': ['kiwify.checkout', 'window.kiwify', 'data-kiwify'],
        'Hotmart': ['hotmart.marketplace', 'window.hotmart', 'data-hotmart'],
    }

    gateways = {
        'Appmax Gateway': ['gateway.appmax.com.br', 'appmax.gateway'],
        'Pagar.me': ['api.pagar.me', 'pagarme.js'],
        'Mercado Pago': ['mercadopago.js', 'secure.mlstatic.com'],
        'PagSeguro': ['pagseguro.uol.com.br', 'pagseguro.directpayment'],
        'Yampi Gateway': ['yampi.gateway'],
        'Stripe': ['checkout.stripe.com', 'js.stripe.com'],
    }

    formas_pagamento = {
        'Pix': ['pix', 'pagamento via pix'],
        'Cartão': ['cartao', 'cartão', 'visa', 'mastercard', 'credito'],
        'Boleto': ['boleto', 'boleto bancário']
    }

    for nome, sinais in checkouts.items():
        if any(p in html for p in sinais):
            resultado['Checkout Detectado'].append(nome)

    for nome, sinais in gateways.items():
        if any(p in html for p in sinais):
            resultado['Gateways Detectados'].append(nome)

    for metodo, sinais in formas_pagamento.items():
        if any(p in html for p in sinais):
            resultado['Formas de Pagamento'].append(metodo)

    for metodo in resultado['Formas de Pagamento']:
        associado = None
        for gateway, sinais in gateways.items():
            for s in sinais:
                if metodo.lower() in s or (s in html and metodo.lower() in html):
                    associado = gateway
                    break
            if associado:
                break
        resultado['Possível Associação'][metodo] = associado if associado else 'Não identificado'

    return resultado

if url:
    if url.startswith('view-source:'):
        url = url.replace('view-source:', '')

    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        html = response.text
        resultado = analisar_checkout(html)
        st.subheader("Resultado da análise")
        st.json(resultado)
    except Exception as e:
        st.error(f"Erro ao processar a URL: {str(e)}")
    