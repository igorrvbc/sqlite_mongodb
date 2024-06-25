"""
    Programa de integração com banco de dados
    utilizando SQLAlchemy e modelo ORM
"""

from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy import Float
from sqlalchemy import create_engine
from sqlalchemy import inspect
from sqlalchemy import select
from sqlalchemy import func

Base = declarative_base()


class Cliente(Base):
    """
        Esta classe representa a tabela Cliente dentro do SQLite.
    """
    __tablename__ = 'cliente'
# Atributos
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String)
    cpf = Column(String(9))
    endereco = Column(String(9))

    conta = relationship(
        "Conta", back_populates="cliente"
    )

    def __repr__(self):
        return f"Cliente(id={self.id}, nome={self.nome}, cpf={self.cpf}, endereço={self.endereco})"


class Conta(Base):
    """
        Esta classe representa a tabela Conta dentro do SQLite.
    """
    __tablename__ = 'conta'
# Atributos
    id = Column(Integer, primary_key=True)
    tipo = Column(String)
    agencia = Column(String)
    num = Column(Integer)
    id_cliente = Column(Integer, ForeignKey('cliente.id'), nullable=False)
    saldo = Column(Float)

    cliente = relationship(
        "Cliente", back_populates="conta"
    )

    def __repr__(self):
        return (f"Conta(id={self.id}, tipo={self.tipo}, agencia={self.agencia}, num={self.num},"
                f" saldo={self.saldo})")


# Conexão com o banco de dados
engine = create_engine("sqlite://")


# Criando as classes como tabelas no banco de dados
Base.metadata.create_all(engine)


# Investiga o esquema do banco de dados
inspetor_engine = inspect(engine)

# Recuperando tabelas criadas
print('Recuperando tabelas criadas:')
print(inspetor_engine.get_table_names())

# Verificando existência de uma tabela específica
print('\nVerificando o schema do banco de dados')
print(inspetor_engine.default_schema_name)

# Persistindo dados nas tabelas
with Session(engine) as session:
    joe = Cliente(
        nome='joe',
        cpf='123123',
        endereco='everywhere',
        conta=[Conta(tipo='conta_corrente', agencia='br', num='123123', saldo='0.0')]
    )

    jolene = Cliente(
        nome='jolene',
        cpf='121212',
        endereco='anywhere',
        conta=[Conta(tipo='conta_salario', agencia='br', num='12312', saldo='100.0')]
    )


# Enviando para o BD
    session.add_all([joe, jolene])

    session.commit()

# Recuperando info a partir do Nome
stmt = select(Cliente).where(Cliente.nome.in_(["joe"]))
print('\nRecuperando usuário a partir de condição de filtragem')
for user in session.scalars(stmt):
    print(user)

# Recuperando informação atraves do id
stmt_conta = select(Conta).where(Conta.id_cliente.in_([1]))
print('\nRecuperando conta a partir de condição de filtragem')
for userid in session.scalars(stmt_conta):
    print(userid)

stmt_order = select(Cliente).order_by(Cliente.nome.desc())
print("\nRecuperando info de maneira ordenada")
for result in session.scalars(stmt_order):
    print(result)

stmt_join = select(Cliente.nome, Conta.tipo).join_from(Conta, Cliente)
print('\n')
for result in session.scalars(stmt_join):
    print(result)

connection = engine.connect()

results = connection.execute(stmt_join).fetchall()
print("\nExecutando statement a partir da connection")
for result in results:
    print(result)

stmt_count = select(func.count('*')).select_from(Cliente)
print("\nTotal de instâncias em Cliente")
for result in session.scalars(stmt_count):
    print(result)
