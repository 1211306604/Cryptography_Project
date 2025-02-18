import string
import time

# ------------------ Playfair Cipher Functions ------------------

def generate_playfair_table(key):
    """
    Creates a 5x5 Playfair table based on the provided key.
    Converts the key to uppercase, removes spaces, and treats 'J' as 'I'.
    Then, it fills in the remaining letters (skipping 'J') and prints the table.
    """
    print("\n══════════════════════════════════════════════════════════")
    print("                  GENERATE PLAYFAIR TABLE                ")
    print("══════════════════════════════════════════════════════════")

    key = key.upper().replace(" ", "")
    table_list = []
    used = set()

    # Add key letters, treating J as I
    for char in key:
        if char == 'J':
            char = 'I'
        if char not in used and char in string.ascii_uppercase:
            used.add(char)
            table_list.append(char)

    # Add the rest of the alphabet (skipping J)
    for char in string.ascii_uppercase:
        if char == 'J':
            continue
        if char not in used:
            used.add(char)
            table_list.append(char)

    # Convert the list into a 5x5 matrix
    matrix = [table_list[i*5:(i+1)*5] for i in range(5)]

    # Display the table
    for row in matrix:
        print(" ".join(row))

    return matrix

def find_position(matrix, letter):
    """
    Searches for a letter in the Playfair table and returns its (row, column) position.
    Treats 'J' as 'I'.
    """
    if letter == 'J':
        letter = 'I'
    for row_idx, row in enumerate(matrix):
        if letter in row:
            return (row_idx, row.index(letter))
    return None

def prepare_text(text, for_encryption=True):
    """
    Cleans and prepares text for the Playfair cipher.
    Removes non-letter characters, converts text to uppercase, replaces 'J' with 'I',
    and splits the text into digrams. If a digram has repeating letters, inserts 'X';
    if the text length is odd, appends 'X' at the end.
    """
    cleaned = "".join(filter(str.isalpha, text.upper()))
    cleaned = cleaned.replace("J", "I")

    if for_encryption:
        prepared = ""
        i = 0
        while i < len(cleaned):
            prepared += cleaned[i]
            if i + 1 < len(cleaned):
                if cleaned[i] == cleaned[i+1]:
                    prepared += 'X'
                    i += 1
                else:
                    prepared += cleaned[i+1]
                    i += 2
            else:
                prepared += 'X'
                i += 1

        print("\n[Playfair] Prepared plaintext (after digram processing):", prepared)
        return prepared
    else:
        return cleaned

def playfair_encrypt(plaintext, key):
    """
    Encrypts the plaintext using the Playfair cipher.
    Displays each digram's encryption step and returns the final ciphertext.
    """
    matrix = generate_playfair_table(key)
    plaintext = prepare_text(plaintext, for_encryption=True)
    ciphertext = ""

    print("\n══════════════════════════════════════════════════════════")
    print("               PLAYFAIR ENCRYPTION DETAILS               ")
    print("══════════════════════════════════════════════════════════")

    for i in range(0, len(plaintext), 2):
        a = plaintext[i]
        b = plaintext[i+1]
        row_a, col_a = find_position(matrix, a)
        row_b, col_b = find_position(matrix, b)

        print(f"Processing digram '{a}{b}' => positions: {a}:(r={row_a}, c={col_a}), {b}:(r={row_b}, c={col_b})", end=" -> ")

        if row_a == row_b:
            enc_a = matrix[row_a][(col_a + 1) % 5]
            enc_b = matrix[row_b][(col_b + 1) % 5]
            ciphertext += enc_a + enc_b
            print(f"Same row -> '{enc_a}{enc_b}'")
        elif col_a == col_b:
            enc_a = matrix[(row_a + 1) % 5][col_a]
            enc_b = matrix[(row_b + 1) % 5][col_b]
            ciphertext += enc_a + enc_b
            print(f"Same column -> '{enc_a}{enc_b}'")
        else:
            enc_a = matrix[row_a][col_b]
            enc_b = matrix[row_b][col_a]
            ciphertext += enc_a + enc_b
            print(f"Rectangle rule -> '{enc_a}{enc_b}'")

    print("\n[Playfair] Final Playfair ciphertext:", ciphertext)
    return ciphertext

def playfair_decrypt(ciphertext, key):
    """
    Decrypts the ciphertext using the Playfair cipher.
    Displays each step of the decryption process and returns the recovered plaintext.
    """
    matrix = generate_playfair_table(key)
    plaintext = ""

    print("\n══════════════════════════════════════════════════════════")
    print("               PLAYFAIR DECRYPTION DETAILS               ")
    print("══════════════════════════════════════════════════════════")

    for i in range(0, len(ciphertext), 2):
        a = ciphertext[i]
        b = ciphertext[i+1]
        row_a, col_a = find_position(matrix, a)
        row_b, col_b = find_position(matrix, b)

        print(f"Processing digram '{a}{b}' => positions: {a}:(r={row_a}, c={col_a}), {b}:(r={row_b}, c={col_b})", end=" -> ")

        if row_a == row_b:
            dec_a = matrix[row_a][(col_a - 1) % 5]
            dec_b = matrix[row_b][(col_b - 1) % 5]
            plaintext += dec_a + dec_b
            print(f"Same row -> '{dec_a}{dec_b}'")
        elif col_a == col_b:
            dec_a = matrix[(row_a - 1) % 5][col_a]
            dec_b = matrix[(row_b - 1) % 5][col_b]
            plaintext += dec_a + dec_b
            print(f"Same column -> '{dec_a}{dec_b}'")
        else:
            dec_a = matrix[row_a][col_b]
            dec_b = matrix[row_b][col_a]
            plaintext += dec_a + dec_b
            print(f"Rectangle rule -> '{dec_a}{dec_b}'")

    print("\n[Playfair] Final Playfair decryption result:", plaintext)
    return plaintext

# ------------------ Rail Fence Cipher Functions ------------------

def rail_fence_encrypt(text, num_rails):
    """
    Encrypts the given text using the Rail Fence cipher.
    It writes the text in a zigzag pattern across the specified number of rails,
    then concatenates the rails to produce the ciphertext.
    Also, it prints the content of each rail.
    """
    print("\n══════════════════════════════════════════════════════════")
    print("                RAIL FENCE ENCRYPTION                    ")
    print("══════════════════════════════════════════════════════════")

    rails = [''] * num_rails
    rail_direction = 1  # +1 means down, -1 means up
    current_rail = 0

    for char in text:
        rails[current_rail] += char
        current_rail += rail_direction
        if current_rail == 0 or current_rail == num_rails - 1:
            rail_direction *= -1

    for idx, rail_text in enumerate(rails):
        print(f"  Rail {idx}: {rail_text}")

    encrypted = "".join(rails)
    print("\n[Rail Fence] Final Rail Fence ciphertext:", encrypted)
    return encrypted

def rail_fence_decrypt(cipher, num_rails):
    """
    Decrypts text encrypted with the Rail Fence cipher.
    It creates a marker matrix to determine the zigzag pattern, visualizes the marker
    before and after inserting the ciphertext characters, and reconstructs the original text.
    """
    print("\n══════════════════════════════════════════════════════════")
    print("                RAIL FENCE DECRYPTION                    ")
    print("══════════════════════════════════════════════════════════")

    n = len(cipher)
    marker = [['' for _ in range(n)] for _ in range(num_rails)]
    rail_direction = 1
    current_rail = 0

    # Mark the zigzag pattern with '*'
    for col in range(n):
        marker[current_rail][col] = '*'
        current_rail += rail_direction
        if current_rail == 0 or current_rail == num_rails - 1:
            rail_direction *= -1

    # Display marker matrix before placing ciphertext
    print("[Rail Fence] Marker matrix (before placing ciphertext):")
    for row in marker:
        print("".join(['*' if x == '*' else '.' for x in row]))

    # Fill the marker positions with ciphertext characters
    idx = 0
    for r in range(num_rails):
        for c in range(n):
            if marker[r][c] == '*':
                marker[r][c] = cipher[idx]
                idx += 1

    # Display the marker matrix after placing characters
    print("\n[Rail Fence] Matrix after placing ciphertext:")
    for row in marker:
        print(" ".join(char if char else '.' for char in row))

    # Read off the matrix in zigzag order to reconstruct the text
    result = []
    rail_direction = 1
    current_rail = 0
    for col in range(n):
        result.append(marker[current_rail][col])
        current_rail += rail_direction
        if current_rail == 0 or current_rail == num_rails - 1:
            rail_direction *= -1

    decrypted = "".join(result)
    print("\n[Rail Fence] Final Rail Fence decryption result:", decrypted)
    return decrypted

# ------------------ Product Cipher Functions ------------------

def product_encrypt(plaintext, playfair_key, rail_fence_num_rails):
    """
    Applies the product cipher by first encrypting the plaintext with the Playfair cipher,
    then encrypting the resulting text with the Rail Fence cipher.
    It also prints timing details for each stage and the total encryption time.
    """
    print("\n══════════════════════════════════════════════════════════")
    print("      PRODUCT ENCRYPTION (Playfair -> Rail Fence)         ")
    print("══════════════════════════════════════════════════════════")

    total_start = time.time()
    
    # Playfair Encryption
    pf_start = time.time()
    playfair_cipher = playfair_encrypt(plaintext, playfair_key)
    pf_end = time.time()
    playfair_time = pf_end - pf_start
    
    # Rail Fence Encryption
    rf_start = time.time()
    final_cipher = rail_fence_encrypt(playfair_cipher, rail_fence_num_rails)
    rf_end = time.time()
    rail_fence_time = rf_end - rf_start

    total_time = time.time() - total_start

    print("\n──────────────────────────────────────────────────────────")
    print(" PRODUCT ENCRYPTION TIMING ")
    print("──────────────────────────────────────────────────────────")
    print(f"Playfair encryption time:   {playfair_time:.6f} s")
    print(f"Rail Fence encryption time: {rail_fence_time:.6f} s")
    print(f"Total encryption time:      {total_time:.6f} s")
    print("\nFinal Product Ciphertext:", final_cipher)

def product_decrypt(ciphertext, playfair_key, rail_fence_num_rails):
    """
    Reverses the product cipher by first decrypting with the Rail Fence cipher,
    then decrypting the resulting text with the Playfair cipher.
    Also prints timing details for each stage and the total decryption time.
    """
    print("\n══════════════════════════════════════════════════════════")
    print("      PRODUCT DECRYPTION (Rail Fence -> Playfair)         ")
    print("══════════════════════════════════════════════════════════")

    total_start = time.time()
    
    # Rail Fence Decryption
    rf_start = time.time()
    rail_decrypted = rail_fence_decrypt(ciphertext, rail_fence_num_rails)
    rf_end = time.time()
    rail_fence_time = rf_end - rf_start
    
    # Playfair Decryption
    pf_start = time.time()
    recovered_text = playfair_decrypt(rail_decrypted, playfair_key)
    pf_end = time.time()
    playfair_time = pf_end - pf_start

    total_time = time.time() - total_start

    print("\n──────────────────────────────────────────────────────────")
    print(" PRODUCT DECRYPTION TIMING ")
    print("──────────────────────────────────────────────────────────")
    print(f"Rail Fence decryption time: {rail_fence_time:.6f} s")
    print(f"Playfair decryption time:   {playfair_time:.6f} s")
    print(f"Total decryption time:      {total_time:.6f} s")
    print("\nRecovered Message:", recovered_text)

# ------------------ Security Notes ------------------

def print_security_notes():
    """
    Prints a brief overview of the security aspects of the Playfair cipher,
    the Rail Fence cipher, and their combination as a product cipher.
    """
    print("\n══════════════════════════════════════════════════════════")
    print("                SECURITY ANALYSIS OVERVIEW               ")
    print("══════════════════════════════════════════════════════════")
    print("- Playfair Cipher:")
    print("  * Uses digram substitution (merging I and J).")
    print("  * More secure than a simple Caesar cipher, but vulnerable")
    print("    to frequency analysis on letter pairs.")
    print("- Rail Fence Cipher:")
    print("  * A basic transposition cipher that rearranges letters in a zigzag pattern,")
    print("    making it susceptible to reconstruction attacks.")
    print("- Product Cipher (Playfair -> Rail Fence):")
    print("  * Combines substitution and transposition for added security,")
    print("    though it remains a classical cipher by modern standards.\n")

# ------------------ Main / Demo ------------------

def main():
    """
    Main function that interacts with the user.
    It prompts the user for encryption or decryption mode, asks for a Playfair key
    (letters only), and a positive number of rails. It then performs the chosen operation
    and displays the final result along with timing and security information.
    """
    print("══════════════════════════════════════════════════════════")
    print("          Product Cipher: Playfair + Rail Fence          ")
    print("══════════════════════════════════════════════════════════")

    # Ask whether to encrypt or decrypt
    while True:
        mode = input("\nType 'E' for encryption or 'D' for decryption: ").strip().upper()
        if mode in ['E', 'D']:
            break
        print("Error: Invalid mode. Please type 'E' or 'D'.")

    # Prompt for a Playfair key (letters only)
    while True:
        playfair_key = input("\nEnter the Playfair key (e.g. MONARCHY, SECRET): ").strip()
        if playfair_key and all(ch.isalpha() or ch.isspace() for ch in playfair_key):
            break
        print("Error: Invalid key. Please enter letters only (e.g., MONARCHY, SECRET).")

    # Ask for the number of rails, ensuring a positive integer is entered
    while True:
        num_rails_input = input("\nEnter the number of rails for Rail Fence (e.g. 3): ").strip()
        if num_rails_input.isdigit():
            num_rails = int(num_rails_input)
            if num_rails > 0:
                break
            else:
                print("Error: Please enter a positive number.")
        else:
            print("Error: Please enter a positive number.")

    # For encryption mode, validate that the plaintext contains at least one letter.
    if mode == 'E':
        while True:
            plaintext = input("\nEnter the plaintext message to encrypt: ").strip()
            if any(ch.isalpha() for ch in plaintext):
                break
            print("Error: Input text must contain at least one alphabetic character.")
        product_encrypt(plaintext, playfair_key, num_rails)
        print("\n===== ENCRYPTION COMPLETE =====")
    else:
        # For decryption, we assume the ciphertext (result from encryption) contains letters.
        ciphertext = input("\nEnter the ciphertext message to decrypt: ").strip()
        if not any(ch.isalpha() for ch in ciphertext):
            print("Error: Input text must contain at least one alphabetic character.")
            return
        product_decrypt(ciphertext, playfair_key, num_rails)
        print("\n===== DECRYPTION COMPLETE =====")

    # Print security summary
    print_security_notes()

if __name__ == "__main__":
    main()
