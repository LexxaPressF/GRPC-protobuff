import grpc
import glossary_pb2
import glossary_pb2_grpc

def run():
    with grpc.insecure_channel('grpc-server:50051') as channel:  # Используйте имя сервиса сервера
        stub = glossary_pb2_grpc.GlossaryServiceStub(channel)

        # Add a term
        print("Adding term 'Python'")
        stub.AddTerm(glossary_pb2.Term(key='Python', description='A popular programming language.'))

        # Get all terms
        print("Getting all terms:")
        response = stub.GetAllTerms(glossary_pb2.Empty())
        for term in response.terms:
            print(f"{term.key}: {term.description}")

        # Get a specific term
        print("Getting term 'Python':")
        term = stub.GetTerm(glossary_pb2.Key(key='Python'))
        print(f"{term.key}: {term.description}")

        # Update the term
        print("Updating term 'Python'")
        stub.UpdateTerm(glossary_pb2.Term(key='Python', description='An awesome programming language.'))

        # Delete the term
        print("Deleting term 'Python'")
        stub.DeleteTerm(glossary_pb2.Key(key='Python'))

if __name__ == '__main__':
    run()
