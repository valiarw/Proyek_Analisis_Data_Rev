import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

file_path = r"Aotizhongxin.csv"

data = pd.read_csv(file_path)
 

st.markdown(
    """
    Bagaimana Konsentrasi Polutan di wilayah Aotizhongxin berdasarkan tren dan pola?
    """
)
data['date'] = pd.to_datetime(data[['year', 'month', 'day']])
data['year'] = data['date'].dt.year
data_filtered = data[data['year'].between(2013, 2017)]
annual_pollutants = data_filtered.groupby('year')[['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']].mean().reset_index()
 
genre = st.selectbox(
    label="Apa yang ingin diketahui?",
    options=('Tren Konsentrasi Polutan', 'Pola musiman pada kualitas udara')
)

st.title('Dashboard :sparkles:')
tab1, tab2, tab3 = st.tabs(["Latar Belakang", "Tren", "Pola"])
 
with tab1:
    st.header("Latar Belakang")
    st.caption('Kualitas udara merupakan salah satu indikator penting yang mempengaruhi kesehatan masyarakat dan lingkungan. Data yang dikumpulkan dari Aotizhongxin, Beijing, selama periode dari Maret 2013 hingga Februari 2017 mencakup konsentrasi berbagai polutan, termasuk PM2.5, PM10, SO2, NO2, CO, dan O3. Pengamatan terhadap perubahan konsentrasi polutan ini sangat penting untuk memahami dampak aktivitas manusia, seperti industri dan transportasi, terhadap kualitas udara. Selain itu, analisis tren tahunan dan pola musiman dari data ini dapat memberikan wawasan yang berharga bagi pengambil kebijakan dalam merancang dan menerapkan strategi pengendalian polusi udara yang lebih efektif. Dengan memahami fluktuasi konsentrasi polutan selama periode ini, kita dapat mengevaluasi efektivitas kebijakan yang ada dan menyesuaikan upaya pengendalian polusi udara untuk meningkatkan kualitas hidup masyarakat.')
 
with tab2:
    st.header('Tren penurunan atau peningkatan Konsentrasi Polutan dari tahun 2013 hingga 2017')

    st.subheader('Rata-rata Tahunan Konsentrasi Polutan')
    st.caption("Tabel ini menunjukan rata-rata tahunan konsentrasi polutan")
    st.dataframe(annual_pollutants)

    st.subheader('Grafik Tren dari Penurunan atau Peningkatan Konsentrasi Polutan dari Tahun 2013 hingga 2017')
    plt.figure(figsize=(12, 6))
    for pollutant in ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']:
        plt.plot(annual_pollutants['year'], annual_pollutants[pollutant], marker='o', label=pollutant)

    plt.title('Tren Konsentrasi Polutan')
    plt.xlabel('Tahun')
    plt.ylabel('Konsentrasi Rata-rata (µg/m³)')
    plt.xticks(annual_pollutants['year'])
    plt.legend(title='Polutan')
    plt.grid(True)
    st.pyplot(plt)
    st.caption('Dari visualisasi tren, kita bisa melihat apakah ada peningkatan atau penurunan konsentrasi polutan dari tahun 2013 ke tahun 2017.')
    st.text("""
      Konsentrasi polutan pada CO mengalami tren penurunan pada tahun 2016, dan mengalami peningkatan pada tahun 2015 dan 2017. Untuk PM10 dan
      PM2.5 cenderung stagnan, namun pada tahun 2016 penurunan dan naik kembali pada tahun 2017. Untuk SO2 dan NO2 dari tahun 2013-2017 tidak
      terjadi tren penurunan ataupun kenaikan. Untuk O3 pada tahun 2015 mengalami kenaikan dan mengalami penurunan pada tahun 2017"""
      )
 
with tab3:
    st.header('Pola Musiman pada Kualitas Udara di Aotizhongxin')

    # Menambahkan kolom 'Season' berdasarkan bulan
    def get_rainy_or_summer(month):
        if month in [6, 7, 8]: 
            return 'Musim Panas'
        elif month in [3, 4, 5]:
            return 'Musim Semi'
        elif month in [12, 1, 2]:
            return 'Musim Dingin'
        else:
            return 'Musim Gugur'

    # Tambahkan kolom 'Season' ke dataset
    data['Season'] = data['month'].apply(get_rainy_or_summer)

    # Menghitung rata-rata polutan berdasarkan musim
    seasonal_pollutants = data.groupby('Season')[['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']].mean()

    st.subheader('Rata-rata konsentrasi polutan di setiap musimnya')
    st.caption("Tabel ini menunjukan rata-rata konsentrasi polutan disetiap musimnya.")
    st.dataframe(seasonal_pollutants)

    st.subheader("Grafik menunjukan adanya pola setiap musimnya")
    st.caption('Grafik yang menunjukan adanya pola setiap musimnya.')
    plt.figure(figsize=(10, 6))
    for pollutant in ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']:
        plt.plot(seasonal_pollutants.index, seasonal_pollutants[pollutant], label=pollutant)

    plt.title('Konsentrasi Polutan Rata-rata Berdasarkan Musim')
    plt.xlabel('Musim', fontsize=1)
    plt.ylabel('Konsentrasi (μg/m³)')
    plt.legend(title='Polutan')
    plt.grid(True)

    # Menampilkan grafik
    plt.show()

    st.pyplot(plt)
    
    st.text("""
            Pola kualitas udara setiap musimnya mengalami perbedaan, seperti pada musim dingin hingga musim panas konsentrasi
            polutan CO mengalami penurunan sedangkan kembali naik pada musim semi. Atau semakin panas kualitas udara CO menurun.
            Sedangkan untuk polutan PM10 kualitas udaranya cenderung sama dari musim dingin ke musim panas dan memiliki kenaikan dari
            musim panas ke musim semi. NO2, SO2 dan PM2.5 setiap musimnya tidak mengalami perubahan/ artinya pergantian musim tidak
            mempengaruhi konsentrasi polutan. Untuk polutan O3 dari musim dingin sampai ke musim semi mengalami kenikan."""
      )


# Menampilkan statistik dasar
st.subheader('Statistik Deskriptif')
st.write(data_filtered[['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']].describe())
