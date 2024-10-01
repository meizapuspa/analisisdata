import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Judul dashboard
st.title("Dashboard E-Commerce")

# Menampilkan logo
st.image('C:\\Users\\meiza\\ecommerce_data\\logo.png', width=150)

# Membaca dataset
customers_df = pd.read_csv('customers_dataset.csv')
orders_df = pd.read_csv('orders_dataset.csv')
order_items = pd.read_csv('order_items_dataset.csv')
order_pay = pd.read_csv('order_payments_dataset.csv')

# Analisis Pertanyaan 1: Pelanggan dengan jumlah pesanan terbanyak
st.subheader("Pelanggan dengan Jumlah Pesanan Terbanyak")
order_counts = orders_df.groupby('customer_id')['order_id'].count().reset_index()
order_counts.columns = ['customer_id', 'order_count']
top_customers = order_counts.sort_values(by='order_count', ascending=False).head(10)

# Visualisasi
plt.figure(figsize=(12, 6))
plt.bar(top_customers['customer_id'].astype(str), top_customers['order_count'], color='skyblue')
plt.title('10 Pelanggan dengan Jumlah Pesanan Terbanyak')
plt.xlabel('Customer ID')
plt.ylabel('Jumlah Pesanan')
plt.xticks(rotation=45)
st.pyplot(plt)

# Menampilkan data pelanggan dengan jumlah pesanan terbanyak
st.write(top_customers)

# Analisis Pertanyaan 2: Pengeluaran rata-rata pelanggan berdasarkan lokasi
st.subheader("Pengeluaran Rata-rata Pelanggan Berdasarkan Lokasi")
total_spending_per_customer = order_pay.groupby('order_id')['payment_value'].sum().reset_index()
order_customer_data = orders_df[['order_id', 'customer_id']]
total_spending_per_customer = total_spending_per_customer.merge(order_customer_data, on='order_id')
total_spending_per_customer = total_spending_per_customer.groupby('customer_id')['payment_value'].sum().reset_index()
customer_data = customers_df
customer_spending = pd.merge(total_spending_per_customer, customer_data, on='customer_id')
average_spending_by_location = customer_spending.groupby('customer_city')['payment_value'].mean().reset_index()

# Visualisasi rata-rata pengeluaran per lokasi
top_cities = average_spending_by_location.nlargest(10, 'payment_value')
plt.figure(figsize=(12, 6))
plt.barh(top_cities['customer_city'], top_cities['payment_value'], color='lightgreen')
plt.title('10 Kota dengan Rata-rata Pengeluaran Pelanggan Tertinggi')
plt.xlabel('Rata-rata Pengeluaran')
plt.ylabel('Kota')
plt.grid(axis='x', linestyle='--', alpha=0.7)
st.pyplot(plt)

# Analisis Pertanyaan 3: Rata-rata pengeluaran per metode pembayaran
st.subheader("Rata-rata Pengeluaran per Metode Pembayaran")
payments_orders = order_pay.merge(orders_df, on='order_id')
total_spending_per_payment = payments_orders.groupby('payment_type')['payment_value'].sum().reset_index()
order_counts_per_payment = payments_orders.groupby('payment_type')['order_id'].nunique().reset_index(name='order_count')
average_spending_per_payment = total_spending_per_payment.merge(order_counts_per_payment, on='payment_type')
average_spending_per_payment['average_spending'] = average_spending_per_payment['payment_value'] / average_spending_per_payment['order_count']

# Visualisasi rata-rata pengeluaran per metode pembayaran
plt.figure(figsize=(10, 6))
sns.barplot(data=average_spending_per_payment, x='payment_type', y='average_spending', palette='viridis')
plt.title('Rata-rata Pengeluaran per Metode Pembayaran')
plt.xlabel('Metode Pembayaran')
plt.ylabel('Rata-rata Pengeluaran')
plt.xticks(rotation=45)
st.pyplot(plt)

# Analisis metode pembayaran yang paling umum digunakan
st.subheader("Metode Pembayaran Paling Umum Digunakan")
payment_summary = order_pay.groupby('payment_type').agg(
    total_transactions=('payment_value', 'count'),
    total_value=('payment_value', 'sum')
).reset_index()

# Visualisasi jumlah transaksi dan total nilai pesanan
fig, axs = plt.subplots(1, 2, figsize=(14, 6))

# Subplot 1: Jumlah Transaksi
sns.barplot(data=payment_summary, x='payment_type', y='total_transactions', palette='Blues', ax=axs[0])
axs[0].set_title('Jumlah Transaksi per Metode Pembayaran', fontsize=16)
axs[0].set_xlabel('Metode Pembayaran', fontsize=14)
axs[0].set_ylabel('Jumlah Transaksi', fontsize=14)
axs[0].tick_params(axis='x', rotation=45)

# Subplot 2: Total Nilai Pesanan
sns.barplot(data=payment_summary, x='payment_type', y='total_value', palette='Oranges', ax=axs[1])
axs[1].set_title('Total Nilai Pesanan per Metode Pembayaran', fontsize=16)
axs[1].set_xlabel('Metode Pembayaran', fontsize=14)
axs[1].set_ylabel('Total Nilai Pesanan', fontsize=14)
axs[1].tick_params(axis='x', rotation=45)

plt.tight_layout()
st.pyplot(fig)

# Visualisasi jumlah transaksi per metode pembayaran (ditampilkan terpisah)
st.subheader("Visualisasi Jumlah Transaksi per Metode Pembayaran")
plt.figure(figsize=(10, 6))
sns.barplot(data=payment_summary, x='payment_type', y='total_transactions', palette='Blues')
plt.title('Jumlah Transaksi per Metode Pembayaran', fontsize=16)
plt.xlabel('Metode Pembayaran', fontsize=14)
plt.ylabel('Jumlah Transaksi', fontsize=14)
plt.xticks(rotation=45)
st.pyplot(plt)

# Copyright
st.markdown("---")
st.write("© 2024 Iza. All rights reserved.")
