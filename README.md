# 🛡️⚽ Sistema de Anonimização Inteligente de Dados de Jogadores

### *Privacidade, IA e DevOps unificados em um único projeto profissional*

Este projeto apresenta um **sistema completo de anonimização de dados**,
aplicado ao contexto esportivo --- mais especificamente, jogadores de
futebol --- utilizando técnicas modernas de **IA**, **generalização**,
**hash criptográfico**, **supressão**, além de **agrupamento por
similaridade (K-Means)** para reforçar privacidade.

Tudo isso é integrado a uma **pipeline CI/CD totalmente automatizada em
GitHub Actions**, que executa geração de dados, anonimização e publica
artifacts em cada commit.

O objetivo final é demonstrar, na prática, como construir um sistema
**seguro**, **automatizado**, **escalável** e com **boas práticas
corporativas** de Engenharia de Software, Dados e DevOps.

------------------------------------------------------------------------

# 🚀 Visão Geral do Sistema

O sistema implementa um fluxo completo:

1.  **Geração de dados sintéticos realistas** de jogadores de futebol\
2.  **Anonimização forte com múltiplas camadas**\
3.  **Agrupamento por similaridade (K-Means)**\
4.  **Pipeline GitHub Actions profissional**

------------------------------------------------------------------------

# 🧠 Arquitetura do Sistema

    /src
     ├── data_gen.py        # Gera dados realistas e sintéticos
     ├── anonymizer.py      # Aplica anonimização + clustering
    /data
     ├── generated_raw_data.csv   # (gerado automaticamente)
     ├── anonymized_data.csv      # (gerado automaticamente)
    /.github/workflows
     ├── pipeline.yml       # Pipeline CI/CD no GitHub Actions

------------------------------------------------------------------------

# ⚙️ Pipeline Automática (GitHub Actions)

A esteira CI/CD executa automaticamente:

1.  Instala dependências\
2.  Gera dados brutos\
3.  Publica artifact `raw-dataset`\
4.  Roda anonimização\
5.  Publica artifact `anonymized-dataset`

------------------------------------------------------------------------

# 🛠️ Como Rodar Localmente

``` bash
git clone https://github.com/SEU_USUARIO/projeto-anonimizacao.git
cd projeto-anonimizacao
pip install pandas numpy scikit-learn faker
python src/data_gen.py
python src/anonymizer.py
```

------------------------------------------------------------------------

# 📦 Arquivos Gerados

  ---------------------------------------------------------------------------------
  Artifact               Arquivo                         Descrição
  ---------------------- ------------------------------- --------------------------
  `raw-dataset`          `data/generated_raw_data.csv`   Dados brutos gerados

  `anonymized-dataset`   `data/anonymized_data.csv`      Dados anonimizados +
                                                         clusters
  ---------------------------------------------------------------------------------

------------------------------------------------------------------------

# 🏆 Conclusão

Este projeto demonstra um sistema profissional que integra IA,
anonimização, segurança de dados e DevOps moderno --- ideal para
demonstração acadêmica, portfolio e ambientes corporativos.
