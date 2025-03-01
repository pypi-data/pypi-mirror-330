import numpy as np
import qrcode
import struct
from pyzbar.pyzbar import decode # requires Visual C++ Redistributable Visual Studio 2013. Install vcredist_x64.exe if using 64-bit Python
from PIL import Image
from transformers import AutoModel, AutoTokenizer
import torch
import base64

class QRVector:

    def __init__(self, model_name="sentence-transformers/all-MiniLM-L6-v2"):
        """
        Initialize QRVector with a specified model for text embedding via transformers.
        
        Args:
            model_name (str): Name of the pre-trained model to use for embeddings
        """
        self.model_name = model_name
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)  # Initialize tokenizer from pre-trained model
        self.model = AutoModel.from_pretrained(model_name)  # Initialize model from pre-trained model

        self.encode_model_name = None
        self.encode_min_val = None
        self.encode_max_val = None
        self.encode_scale = None
        self.encode_quantized = None

        self.decode_model_name = None
        self.decode_min_val = None
        self.decode_max_val = None
        self.decode_scale = None
        self.decode_quantized = None
        
    def get_embedding(self, text):
        """
        Generate an embedding vector for the given text using the pre-trained model.
        
        Args:
            text (str): The input text to be embedded.
        
        Returns:
            np.ndarray: A numpy array representing the embedding vector of the input text.
        """
        inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True)  # Tokenize input text
        with torch.no_grad():
            outputs = self.model(**inputs)  # Get model outputs without computing gradients
        return outputs.last_hidden_state.mean(dim=1).squeeze().cpu().numpy().astype(np.float32)  # Return mean of last hidden state as numpy array

    def _encode_vector_to_binary(self, model_name, vector):
        """
        Encode a vector into binary format with correct quantization.
        
        Args:
            model_name (str): The name of the model used for embedding.
            vector (np.ndarray): The embedding vector to encode.
        
        Returns:
            bytes: The binary representation of the encoded vector.
        
        The values like 'B', '<H', '<f', '<I', etc., are format specifiers used in Python's struct module. This module is used for working with C-style binary data, allowing you to pack and unpack data into and from binary formats. Here's what each of these specifiers represents:
        - 'B': This represents an unsigned char (8-bit integer). It is used to pack or unpack a single byte of data.
        - '<H': This represents an unsigned short (16-bit integer) in little-endian byte order. The < indicates little-endian, which is the byte order where the least significant byte is stored first.
        - '<f': This represents a float (32-bit floating point number) in little-endian byte order. Again, the < indicates little-endian.
        - '<I': This represents an unsigned int (32-bit integer) in little-endian byte order. Used here for storing the total length of the binary data.

        These format specifiers are used in the struct.pack and struct.unpack functions to convert between Python values and C structs represented as Python bytes objects.
        """
        N = len(model_name)  # Length of model name
        D = len(vector)  # Dimension of the vector
        min_val = vector.min()  # Minimum value in the vector
        max_val = vector.max()  # Maximum value in the vector
        scale = (max_val - min_val) / 255 if max_val != min_val else 1.0  # Calculate scale for quantization
        quantized = np.round(np.clip((vector - min_val) / scale, 0, 255)).astype(np.uint8)  # Quantize vector: clip to [0, 255] after scaling

        self.encode_model_name = model_name
        self.encode_min_val = min_val
        self.encode_max_val = max_val
        self.encode_scale = scale
        self.encode_quantized = quantized
        
        binary_data = (
            struct.pack('B', N) +  # Pack length of model name
            model_name.encode('utf-8') +  # Encode model name
            struct.pack('B', 1) +  # encoding_type = 1 for uint8
            struct.pack('<H', D) +  # Pack dimension of vector
            struct.pack('<f', min_val) +  # Pack minimum value
            struct.pack('<f', scale) +  # Pack scale
            quantized.tobytes()  # Convert quantized vector to bytes
        )
        total_length = len(binary_data) + 4  # Calculate total length of binary data
        return struct.pack('<I', total_length) + binary_data  # Return packed binary data

    def _decode_binary_to_vector(self, binary_data):
        """
        Decode binary data back to model name and vector.
        
        Args:
            binary_data (bytes): The binary data to decode.
        
        Returns:
            tuple: A tuple containing the model name (str) and the decoded vector (np.ndarray).
        
        The values like 'B', '<H', '<f', '<I', etc., are format specifiers used in Python's struct module. 
        This module is used for working with C-style binary data, allowing you to pack and unpack data into and from binary formats. 
        Here's what each of these specifiers represents:
        - 'B': This represents an unsigned char (8-bit integer). It is used to pack or unpack a single byte of data.
        - '<H': This represents an unsigned short (16-bit integer) in little-endian byte order.
        - '<f': This represents a float (32-bit floating point number) in little-endian byte order.
        - '<I': This represents an unsigned int (32-bit integer) in little-endian byte order. Used here for reading the total length of the binary data.
        - The < indicates little-endian, which is the byte order where the least significant byte is stored first.
        """
        total_length = struct.unpack('<I', binary_data[0:4])[0]  # Unpack total length of binary data
        if total_length != len(binary_data):
            raise ValueError(f"Binary data length mismatch: expected {total_length}, got {len(binary_data)}")
        
        offset = 4  # Initialize offset for reading binary data
        N = struct.unpack('B', binary_data[offset:offset+1])[0]  # Unpack length of model name
        offset += 1
        model_name = binary_data[offset:offset+N].decode('utf-8')  # Decode model name
        offset += N
        encoding_type = struct.unpack('B', binary_data[offset:offset+1])[0]  # Unpack encoding type
        offset += 1
        D = struct.unpack('<H', binary_data[offset:offset+2])[0]  # Unpack dimension of vector
        offset += 2
        min_val = struct.unpack('<f', binary_data[offset:offset+4])[0]  # Unpack minimum value
        offset += 4
        scale = struct.unpack('<f', binary_data[offset:offset+4])[0]  # Unpack scale
        offset += 4
        
        if encoding_type != 1:
            raise ValueError("Unsupported encoding type")
        
        quantized = np.frombuffer(binary_data[offset:offset+D], dtype=np.uint8)  # Read quantized vector

        self.decode_model_name = model_name
        self.decode_min_val = min_val
        self.decode_max_val = min_val + 255 * scale
        self.decode_scale = scale
        self.decode_quantized = quantized
        
        vector = min_val + quantized.astype(np.float32) * scale  # Dequantize vector
        return model_name, vector  # Return model name and dequantized vector

    def generate_qr_code(self, vector, output_filename="embedding_qr.png"):
        """
        Generate a QR code from a vector, using base64 encoding.
        
        Args:
            vector (np.ndarray): The embedding vector to encode into the QR code.
            output_filename (str): The filename for the output QR code image.
        
        Returns:
            img: The generated QR code image.
        """
        binary_data = self._encode_vector_to_binary(self.model_name, vector)  # Encode vector to binary
        base64_data = base64.b64encode(binary_data).decode('utf-8')  # Encode binary data to base64
        
        qr = qrcode.QRCode(
            version=None,  # Automatic version selection
            error_correction=qrcode.constants.ERROR_CORRECT_L,  # Low error correction
            box_size=10,  # Size of each box in the QR code
            border=4,  # Border size
        )
        qr.add_data(base64_data, optimize=0)  # Add data to QR code
        qr.make(fit=True)  # Fit data into QR code
        img = qr.make_image(fill_color="black", back_color="white")  # Create QR code image
        img.save(output_filename, format="PNG")  # Save image as PNG
        return img

    def read_qr_code(self, image_path):
        """
        Read a QR code and decode the vector.
        
        Args:
            image_path (str): The path to the image file containing the QR code.
        
        Returns:
            tuple: A tuple containing the model name (str) and the decoded vector (np.ndarray).
        """
        img = Image.open(image_path)  # Open image file
        decoded_objs = decode(img)  # Decode QR code from image
        if not decoded_objs:
            raise ValueError("No QR code found in image")
        if len(decoded_objs) > 1:
            raise ValueError("Multiple QR codes found; expected one")
        
        base64_data = decoded_objs[0].data.decode('utf-8')  # Decode base64 data from QR code
        binary_data = base64.b64decode(base64_data)  # Decode binary data from base64
        return self._decode_binary_to_vector(binary_data)  # Decode binary data to vector 