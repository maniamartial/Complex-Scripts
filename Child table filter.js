    onload: function(frm, cdt, cdn) {
        items = (frm.doc.custom_items || [])
      
        frm.set_query("barcode", "custom_items", (frm, cdt, cdn) => {
            const row = locals[cdt][cdn];
            const selected_barcodes = items
                .filter(r => r.name !== cdn && r.barcode)
                .map(r => r.barcode);

            return {
                filters: {
                    "item_code": row.item_code,
                    "batch": row.batch_no || undefined,
                    "sold": 0,
                    "name": ["not in", selected_barcodes]
                },
            };
        });
        frm.refresh_field("custom_items");
        frm.refresh();

    }
,    
