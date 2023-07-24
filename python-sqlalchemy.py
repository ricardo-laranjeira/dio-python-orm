from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy.orm import relationship
from sqlalchemy import Column
from sqlalchemy import create_engine
from sqlalchemy import inspect
from sqlalchemy import select
from sqlalchemy import func
from sqlalchemy import Integer
from sqlalchemy import Float
from sqlalchemy import String
from sqlalchemy import ForeignKey

Base = declarative_base()

class Cliente(Base):
    __tablename__ = "cliente"
    id = Column(Integer, primary_key=True)
    nome = Column(String)
    cpf = Column(String)
    endereco = Column(String)
    conta = relationship(
        "Conta", back_populates="cliente", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"Cliente(id={self.id}, nome={self.nome}, cpf={self.cpf}, endereco={self.endereco})"


class Conta(Base):
    __tablename__ = "conta"
    id = Column(Integer, primary_key=True)
    tipo = Column(String, nullable=False)
    numero = Column(Integer, nullable=False)
    saldo = Column(Float, nullable=False)
    id_cliente = Column(Integer, ForeignKey("cliente.id"), nullable=False)

    cliente = relationship("Cliente", back_populates="conta")

    def __repr__(self):
        return f"Conta(id={self.id}, tipo={self.tipo}, numero={self.numero}, saldo={self.saldo}, cliente={self.id_cliente})"


engine = create_engine("sqlite://")
Base.metadata.create_all(engine)

# investiga o esquema de banco de dados
"""inspetor_engine = inspect(engine)
print(inspetor_engine.has_table("user_account"))
print(inspetor_engine.get_table_names())
print(inspetor_engine.default_schema_name)"""

with Session(engine) as session:
    maria = Cliente(
        nome='Maria',
        cpf='111.111.111-11',
        endereco='Rua Helio Gracie, 34',
        conta=[Conta(tipo='CC', numero='4525-9',saldo=452.35)]
    )

    helena = Cliente(
        nome='Helena',
        cpf='222.222.222-22',
        endereco='Avenida Jorge Amado, 78',
        conta=[Conta(tipo='CC', numero='8544-9',saldo=658.35),
                Conta(tipo='CS', numero='6321-9',saldo=1200.35)]
    )

    pedro = Cliente(nome='Pedro', cpf='333.333.333-33', endereco='Rua Amador Bueno, 35')
    
    session.add_all([maria, helena, pedro])

    session.commit()

    stmt = select(Cliente).where(Cliente.nome.in_(["Maria", 'Helena']))
    print('Recuperando usuários a partir de condição de filtragem')
    for cliente in session.scalars(stmt):
        print(cliente)


    stmt_conta = select(Conta).where(Conta.id_cliente.in_([2]))
    print('\nRecuperando a conta de Helena')
    for conta in session.scalars(stmt_conta):
        print(conta)


    stmt_order = select(Cliente).order_by(Cliente.nome.desc())
    print("\nRecuperando info de maneira ordenada")
    for result in session.scalars(stmt_order):
        print(result)

    stmt_join = select(Cliente.nome, Conta.numero).join_from(Conta, Cliente)
    print("\n")
    for result in session.scalars(stmt_join):
        print(result)

    # print(select(User.fullname, Address.email_address).join_from(Address, User))

    connection = engine.connect()
    results = connection.execute(stmt_join).fetchall()
    print("\nExecutando statement a partir da connection")
    for result in results:
        print(result)

    stmt_count = select(func.count('*')).select_from(Cliente)
    print('\nTotal de instâncias em Cliente')
    for result in session.scalars(stmt_count):
        print(result)

session.close()