from sqlalchemy import create_engine

# Corrected DATABASE_URL
DATABASE_URL = "postgresql://uf0rv178g9m2jt:p5a4a30d17f5db8a6deea11e0feacb3669d38349234aeaafaa92138b4bbc8280d@c7u1tn6bvvsodf.cluster-czz5s0kz4scl.eu-west-1.rds.amazonaws.com:5432/df95g2gfqmjlvq"

try:
    # Create an engine
    engine = create_engine(DATABASE_URL)

    # Test the connection
    with engine.connect() as connection:
        result = connection.execute("SELECT 1")
        print("Connection successful:", result.fetchone())
except Exception as e:
    print("Error:", e)
