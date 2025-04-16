def get_private_key(key_file_path, e_settings):
    try:
        if key_file_path.startswith('/private/files/'):
            file_name = key_file_path.split('/')[-1]
            
            file_docs = frappe.get_all("File", filters={"file_name": file_name}, fields=["name"])
            if file_docs:
                # Use Frappe's file manager to get the file content
                key_file_path = file_docs[0].name 
                fname, pfx_data = frappe.utils.file_manager.get_file(key_file_path)
            else:
                # find the file in Frappe's database
                file_doc = frappe.get_doc("File", {"file_name": file_name})
                if file_doc:
                    # Get file content through the File document
                    fname, pfx_data = frappe.utils.file_manager.get_file(file_doc.name)
                else:
                    raise Exception(f"Certificate file {file_name} not found in the system")
        
        private_key_password = get_mode_decrypted_password(e_settings)
        password_bytes = private_key_password.encode('utf-8') if private_key_password else b""
        
        pfx = pkcs12.load_key_and_certificates(pfx_data, password_bytes, default_backend())
        private_key = pfx[0]
        
        if private_key is None:
            raise Exception("Private key extraction failed: private_key is None")
            
        return private_key
