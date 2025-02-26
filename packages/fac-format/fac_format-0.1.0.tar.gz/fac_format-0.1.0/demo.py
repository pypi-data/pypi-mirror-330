from fac_format import FacParser, FacWriter

def main():
    print("Reading FAC file:")
    with open('example.fac', 'r') as f:
        content = f.read()

    parser = FacParser()
    data = parser.parse(content)
    print("Parsed data:", data)
    print("\n" + "="*50 + "\n")

    print("Writing FAC file:")
    test_data = {
        "name": "Jane Smith",
        "age": 25,
        "is_student": True,
        "grades": ["A", "B+", "A-"],
        "contact": {
            "email": "jane@example.com",
            "phone": "555-0123"
        }
    }

    writer = FacWriter()
    fac_content = writer.write(test_data)
    print(fac_content)

if __name__ == "__main__":
    main()