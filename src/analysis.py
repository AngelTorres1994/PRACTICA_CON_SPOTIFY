import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def load_data(file_path = r"C:\Users\angel\Downloads\spotify-mini-analysis\spotify-mini-analysis\data\tu_top_de_canciones_2024.csv"
, sep=','):
    """
    Carga un archivo CSV desde la ruta especificada (por defecto: top de Spotify).
    """
    try:
        df = pd.read_csv(file_path, sep=sep)
        print(f"✅ Archivo cargado correctamente: {file_path}")
        return df
    except Exception as e:
        print(f"❌ Error al cargar el archivo: {e}")
        return None

def top_artists(df, n=10):
    return df['Artist Name(s)'].value_counts().head(n)

def top_genres(df, n=10):
    all_genres = df['Genres'].dropna().str.split(',').explode()
    return all_genres.str.strip().value_counts().head(n)

def top_songs_by_popularity(df, n=10):
    return df[['Track Name', 'Artist Name(s)', 'Popularity']].sort_values(by='Popularity', ascending=False).head(n)

def audio_feature_stats(df):
    audio_columns = ['Danceability', 'Energy', 'Valence', 'Loudness', 'Tempo']
    return df[audio_columns].describe()

def filter_by_energy(df, threshold=0.8):
    return df[df['Energy'] >= threshold][['Track Name', 'Artist Name(s)', 'Energy']].sort_values(by='Energy', ascending=False)

def filter_by_valence(df, threshold=0.2):
    return df[df['Valence'] <= threshold][['Track Name', 'Artist Name(s)', 'Valence']].sort_values(by='Valence')

def most_danceable(df, n=10):
    return df[['Track Name', 'Artist Name(s)', 'Danceability']].sort_values(by='Danceability', ascending=False).head(n)

def average_duration_minutes(df):
    return df['Duration (ms)'].mean() / 60000

# 🎬 EJECUCIÓN DIRECTA
if __name__ == "__main__":
    df = load_data()

    if df is not None:
        print("\n Top artistas:")
        print(top_artists(df))

        print("\n Top géneros:")
        print(top_genres(df))

        print("\n Canciones más populares:")
        print(top_songs_by_popularity(df))

        print("\n Estadísticas de audio:")
        print(audio_feature_stats(df))

        print("\n Canciones más bailables:")
        print(most_danceable(df))

        print("\nCanciones más tristes (valence bajo):")
        print(filter_by_valence(df))

        print(f"\n⏱️ Duración promedio de canciones: {average_duration_minutes(df):.2f} minutos")

sns.boxplot(x=df['Release Date'].astype(str).str[:4].astype(int))
plt.title("📦 Boxplot de Años de Lanzamiento")
plt.xlabel("Año")
plt.tight_layout()
plt.show()


# Asegurarse de que los años están bien formateados como enteros
df['Year'] = df['Release Date'].astype(str).str[:4].astype(int)

# Crear la figura
plt.figure(figsize=(10, 2))
box = sns.boxplot(x=df['Year'], color="skyblue")

# Calcular los valores que usa el boxplot (mínimo, Q1, mediana, Q3, máximo, etc.)
quartiles = np.percentile(df['Year'], [0, 20, 40, 60, 80, 100])

# Dibujar líneas de corte y anotarlas
for q in quartiles:
    plt.axvline(q, color='gray', linestyle='--', alpha=0.5)
    plt.text(q, 0.02, str(int(q)), rotation=90, va='bottom', ha='center', fontsize=8)

# Estética final
plt.title("📦 Boxplot de Años de Lanzamiento (6 cortes: 0%, 20%, ..., 100%)")
plt.xlabel("Año")
plt.yticks([])  # ocultar eje Y porque no es necesario
plt.tight_layout()
plt.show()