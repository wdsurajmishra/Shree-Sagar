def capitalize_full_name(full_name):
    return ' '.join(word.capitalize() for word in full_name.split())

# Example usage
if __name__ == "__main__":
    full_name = input().strip()
    capitalized_name = capitalize_full_name(full_name)
    print(capitalized_name)
