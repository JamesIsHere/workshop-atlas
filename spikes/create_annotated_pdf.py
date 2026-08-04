import fitz

doc = fitz.open('forms/g-28.pdf')

for page_index in range(len(doc)):
    page = doc[page_index]
    widgets = page.widgets()
    if not widgets:
        continue
    
    for w in widgets:
        rect = w.rect
        field_name = w.field_name or ''
        # Shorten XFA style names for visual clarity if needed, or keep full
        short_name = field_name.split('.')[-1] if '.' in field_name else field_name
        
        # Draw red rectangle around field box
        shape = page.new_shape()
        shape.draw_rect(rect)
        shape.finish(color=(1, 0, 0), width=0.8, fill=(1, 1, 0), fill_opacity=0.15)
        shape.commit()
        
        # Insert field name text above/on the box
        page.insert_text(
            fitz.Point(rect.x0, max(rect.y0 - 2, 10)),
            short_name,
            fontsize=6,
            color=(0.8, 0, 0)
        )

doc.save('forms/g-28_annotated.pdf')
print("Saved annotated PDF: forms/g-28_annotated.pdf")

# Render page 0 as image for inspection/embedding
doc_annot = fitz.open('forms/g-28_annotated.pdf')
page0 = doc_annot[0]
pix = page0.get_pixmap(dpi=150)
pix.save('forms/g-28_page1_annotated.png')
print("Saved page 1 preview: forms/g-28_page1_annotated.png")
