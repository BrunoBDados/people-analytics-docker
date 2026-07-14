import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# ---------- EXTRACT ----------
def extract_data(filepath):
    print("Lendo o dataset...")
    df = pd.read_csv(filepath)
    print(f"Dataset carregado: {df.shape[0]} linhas, {df.shape[1]} colunas")
    return df

# ---------- TRANSFORM ----------
def transform_data(df):
    print("Transformando dados...")
    
    colunas = [
        'Age', 'Attrition', 'Department', 'DistanceFromHome',
        'JobSatisfaction', 'MonthlyIncome', 'OverTime',
        'TotalWorkingYears', 'YearsAtCompany', 'JobRole'
    ]
    df = df[colunas].copy()
    
    df.rename(columns={
        'Age': 'Idade',
        'Attrition': 'Saiu_Empresa',
        'Department': 'Departamento',
        'DistanceFromHome': 'Distancia_Casa_KM',
        'JobSatisfaction': 'Satisfacao_Trabalho',
        'MonthlyIncome': 'Salario_Mensal',
        'OverTime': 'Faz_Hora_Extra',
        'TotalWorkingYears': 'Anos_Experiencia',
        'YearsAtCompany': 'Anos_Empresa',
        'JobRole': 'Cargo'
    }, inplace=True)
    
    df['Saiu_Empresa'] = df['Saiu_Empresa'].map({'Yes': 1, 'No': 0})
    df['Faz_Hora_Extra'] = df['Faz_Hora_Extra'].map({'Yes': 1, 'No': 0})
    
    print("Transformação concluída")
    return df

# ---------- LOAD ----------
def load_data(df, output_path):
    print(f"Salvando resultado em {output_path}...")
    df.to_csv(output_path, index=False)
    print("Dados tratados salvos com sucesso!")

# ---------- VISUALIZE ----------
def generate_charts(df, output_dir):
    print("Gerando gráficos...")
    os.makedirs(output_dir, exist_ok=True)
    sns.set_style("whitegrid")
    
    # Gráfico 1: Attrition por Departamento
    plt.figure(figsize=(8, 5))
    attrition_dept = df.groupby('Departamento')['Saiu_Empresa'].mean().sort_values(ascending=False) * 100
    attrition_dept.plot(kind='bar', color='#c0392b')
    plt.title('Taxa de Saída (%) por Departamento')
    plt.ylabel('% de Funcionários que Saíram')
    plt.xlabel('Departamento')
    plt.xticks(rotation=30, ha='right')
    plt.tight_layout()
    plt.savefig(f'{output_dir}/attrition_por_departamento.png')
    plt.close()
    
    # Gráfico 2: Satisfação vs Attrition
    plt.figure(figsize=(8, 5))
    sns.countplot(data=df, x='Satisfacao_Trabalho', hue='Saiu_Empresa', palette=['#2980b9', '#c0392b'])
    plt.title('Satisfação no Trabalho vs Saída da Empresa')
    plt.xlabel('Nível de Satisfação (1=Baixa, 4=Alta)')
    plt.ylabel('Número de Funcionários')
    plt.legend(title='Saiu da Empresa', labels=['Não', 'Sim'])
    plt.tight_layout()
    plt.savefig(f'{output_dir}/satisfacao_vs_attrition.png')
    plt.close()
    
    # Gráfico 3: Hora Extra vs Attrition
    plt.figure(figsize=(8, 5))
    overtime_attrition = df.groupby('Faz_Hora_Extra')['Saiu_Empresa'].mean() * 100
    overtime_attrition.index = ['Não faz', 'Faz hora extra']
    overtime_attrition.plot(kind='bar', color='#e67e22')
    plt.title('Taxa de Saída (%) por Hora Extra')
    plt.ylabel('% de Funcionários que Saíram')
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(f'{output_dir}/hora_extra_vs_attrition.png')
    plt.close()
    
    print("Gráficos gerados com sucesso!")

# ---------- MAIN ----------
if __name__ == "__main__":
    input_path = "/app/data/WA_Fn-UseC_-HR-Employee-Attrition.csv"
    output_path = "/app/data/hr_analytics_tratado.csv"
    charts_dir = "/app/data/charts"
    
    df = extract_data(input_path)
    df = transform_data(df)
    load_data(df, output_path)
    generate_charts(df, charts_dir)
    
    print("Pipeline finalizado com sucesso!")