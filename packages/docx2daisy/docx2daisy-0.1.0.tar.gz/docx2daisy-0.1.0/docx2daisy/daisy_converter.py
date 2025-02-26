import os
import uuid
import zipfile
from xml.etree import ElementTree as ET
from docx import Document


def extract_images_from_doc(doc):
    """
    Extract images from the document's relationships.
    Returns a dictionary mapping relationship IDs to image info:
    {rId: {"filename": filename, "data": binary_data, "content_type": ct}, ...}
    """
    image_mapping = {}
    image_counter = 1
    for rel in doc.part.rels.values():
        if "image" in rel.reltype:
            ct = rel.target_part.content_type  # e.g., "image/jpeg"
            ext = {
                "image/jpeg": ".jpg",
                "image/png": ".png",
                "image/gif": ".gif",
                "image/bmp": ".bmp",
            }.get(ct, ".img")
            filename = f"image{image_counter}{ext}"
            image_mapping[rel.rId] = {
                "filename": filename,
                "data": rel.target_part.blob,
                "content_type": ct
            }
            image_counter += 1
    return image_mapping


def extract_images_from_run(run, image_mapping):
    """
    Search for images embedded within a run element.
    If found, retrieve the corresponding filename and alternative text (if available)
    using the embed id from the image_mapping. Returns a list of image info dictionaries.
    """
    images = []
    # Define namespaces (using findall() with explicit namespace in tag)
    ns_a = "http://schemas.openxmlformats.org/drawingml/2006/main"
    ns_wp = "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"
    # Find all <a:blip> elements within the run
    blips = run._element.findall('.//{%s}blip' % ns_a)
    for blip in blips:
        embed = blip.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed')
        if embed in image_mapping:
            # Get alt text from wp:docPr element's 'descr' attribute if available
            docPrs = run._element.findall('.//{%s}docPr' % ns_wp)
            alt = ""
            if docPrs and 'descr' in docPrs[0].attrib:
                alt = docPrs[0].attrib.get('descr')
            images.append({
                "rId": embed,
                "filename": image_mapping[embed]["filename"],
                "alt": alt if alt else "Image"
            })
    return images


def docx_to_daisy(docx_path, output_zip_path):
    """
    Convert a .docx file to a DAISY 3 text+image book packaged as a ZIP file.
    """
    # 1. Parse the .docx and extract metadata
    doc = Document(docx_path)
    properties = doc.core_properties
    title = properties.title if properties.title else os.path.splitext(os.path.basename(docx_path))[0]
    creator = properties.author if properties.author else "Unknown"
    language = properties.language if properties.language else "en-US"

    # 2. Extract all images contained in the document
    image_mapping = extract_images_from_doc(doc)

    # 3. Create the DTBook (XML) document
    dtbook_elem = ET.Element("dtbook", {
        "version": "2005-3",
        "xml:lang": language
    })
    # Create head metadata
    head_elem = ET.SubElement(dtbook_elem, "head")
    ET.SubElement(head_elem, "meta", {"name": "dc:Title", "content": title})
    ET.SubElement(head_elem, "meta", {"name": "dc:Creator", "content": creator})
    ET.SubElement(head_elem, "meta", {"name": "dc:Language", "content": language})
    ET.SubElement(head_elem, "meta", {"name": "dc:Format", "content": "ANSI/NISO Z39.86-2005"})

    # Create book element and bodymatter
    book_elem = ET.SubElement(dtbook_elem, "book")
    bodymatter = ET.SubElement(book_elem, "bodymatter")

    # Prepare navigation points for NCX
    nav_points = []  # Each item: (level, text, xml_id, playorder)
    play_order = 1
    level_stack = []  # Stack to manage open levels: (level_number, xml_element)
    current_list_elem = None  # Flag for handling lists

    def close_levels_down_to(target_level):
        nonlocal level_stack
        while level_stack and level_stack[-1][0] >= target_level:
            level_stack.pop()

    # Process each paragraph in the document
    for para in doc.paragraphs:
        style = para.style.name if para.style else ""
        # Check if the paragraph is a heading (e.g., "Heading 1", "Heading 2", etc.)
        if style.startswith("Heading"):
            if current_list_elem is not None:
                current_list_elem = None  # End current list
            try:
                level = int(style.split()[1])
            except:
                level = 1
            if level_stack and level_stack[-1][0] >= level:
                close_levels_down_to(level)
            prev_level = level_stack[-1][0] if level_stack else 0
            for new_level in range(prev_level + 1, level + 1):
                level_elem = ET.SubElement(bodymatter if not level_stack else level_stack[-1][1],
                                           f"level{new_level}")
                level_stack.append((new_level, level_elem))
            level_elem = level_stack[-1][1]
            sec_id = f"nav{play_order}"
            level_elem.set("id", sec_id)
            h_tag = ET.SubElement(level_elem, f"h{level}")
            h_tag.text = para.text.strip()
            nav_points.append((level, para.text.strip(), sec_id, play_order))
            play_order += 1
            continue

        # Process non-heading paragraphs
        if "List" in style or (para.style.base_style and "List" in para.style.base_style.name):
            list_type = "unordered"
            if "Number" in style or "number" in style.lower():
                list_type = "ordered"
            if current_list_elem is None:
                current_list_elem = ET.SubElement(level_stack[-1][1] if level_stack else bodymatter,
                                                  "list",
                                                  {"type": "unordered" if list_type == "unordered" else "ordered"})
            item_elem = ET.SubElement(current_list_elem, "item")
            p_elem = ET.SubElement(item_elem, "p")
        else:
            if current_list_elem is not None:
                current_list_elem = None
            if not level_stack:
                # If no heading exists, create an implicit level1 container
                level_elem = ET.SubElement(bodymatter, "level1")
                level_stack.append((1, level_elem))
            p_elem = ET.SubElement(level_stack[-1][1], "p")

        # Process each run in the paragraph for text and images
        for run in para.runs:
            run_text = run.text
            if run_text:
                if p_elem.text is None:
                    p_elem.text = run_text
                else:
                    if len(p_elem) > 0:
                        if p_elem[-1].tail:
                            p_elem[-1].tail += run_text
                        else:
                            p_elem[-1].tail = run_text
                    else:
                        p_elem.text += run_text
            imgs = extract_images_from_run(run, image_mapping)
            for img in imgs:
                # Insert an image via a mediaobject element
                media_elem = ET.Element("mediaobject")
                image_obj = ET.SubElement(media_elem, "imageobject")
                ET.SubElement(image_obj, "imagedata", {
                    "src": f"images/{img['filename']}",
                    "alt": img.get("alt", "Image")
                })
                p_elem.append(media_elem)

    dtbook_xml_str = '<?xml version="1.0" encoding="UTF-8"?>\n'
    dtbook_xml_str += '<!DOCTYPE dtbook PUBLIC "-//NISO//DTD dtbook 2005-3//EN" "http://www.daisy.org/z3986/2005/dtbook-2005-3.dtd">\n'
    dtbook_xml_str += ET.tostring(dtbook_elem, encoding="utf-8").decode("utf-8")

    # 4. Create NCX file with DOCTYPE declaration
    NCX_NS = "http://www.daisy.org/z3986/2005/ncx/"
    ncx_elem = ET.Element("ncx", {"xmlns": NCX_NS, "version": "2005-1"})
    ncx_head = ET.SubElement(ncx_elem, "head")
    ET.SubElement(ncx_head, "meta", {"name": "dtb:uid", "content": str(uuid.uuid4())})
    depth = str(max([lvl for lvl, _, _, _ in nav_points]) if nav_points else 1)
    ET.SubElement(ncx_head, "meta", {"name": "dtb:depth", "content": depth})
    ET.SubElement(ncx_head, "meta", {"name": "dtb:generator", "content": "docx-to-daisy-python"})
    ET.SubElement(ncx_head, "meta", {"name": "dtb:totalPageCount", "content": "0"})
    ET.SubElement(ncx_head, "meta", {"name": "dtb:maxPageNumber", "content": "0"})
    docTitle = ET.SubElement(ncx_elem, "docTitle")
    ET.SubElement(docTitle, "text").text = title
    docAuthor = ET.SubElement(ncx_elem, "docAuthor")
    ET.SubElement(docAuthor, "text").text = creator
    navMap = ET.SubElement(ncx_elem, "navMap")
    nav_stack = []
    for level, txt, sec_id, order in nav_points:
        navPoint = ET.Element("navPoint", {
            "id": f"nav{order}",
            "playOrder": str(order),
            "class": f"level{level}"
        })
        navLabel = ET.SubElement(navPoint, "navLabel")
        ET.SubElement(navLabel, "text").text = txt
        ET.SubElement(navPoint, "content", {"src": f"book.smil#{sec_id}"})
        if not nav_stack:
            navMap.append(navPoint)
            nav_stack.append((level, navPoint))
        else:
            if level > nav_stack[-1][0]:
                nav_stack[-1][1].append(navPoint)
                nav_stack.append((level, navPoint))
            else:
                while nav_stack and nav_stack[-1][0] >= level:
                    nav_stack.pop()
                if not nav_stack:
                    navMap.append(navPoint)
                    nav_stack.append((level, navPoint))
                else:
                    nav_stack[-1][1].append(navPoint)
                    nav_stack.append((level, navPoint))
    ncx_xml_str = '<?xml version="1.0" encoding="UTF-8"?>\n'
    ncx_xml_str += '<!DOCTYPE ncx PUBLIC "-//NISO//DTD ncx 2005-1//EN" "http://www.daisy.org/z3986/2005/ncx-2005-1.dtd">\n'
    ncx_xml_str += ET.tostring(ncx_elem, encoding="utf-8").decode("utf-8")

    # 5. Create SMIL file with DOCTYPE and an empty <audio> element for each nav point
    smil_elem = ET.Element("smil", {"xmlns": "http://www.w3.org/2001/SMIL20/Language"})
    smil_head = ET.SubElement(smil_elem, "head")
    ET.SubElement(smil_head, "meta", {"name": "dc:Title", "content": title})
    smil_body = ET.SubElement(smil_elem, "body")
    seq_elem = ET.SubElement(smil_body, "seq")
    for level, txt, sec_id, order in nav_points:
        par_elem = ET.SubElement(seq_elem, "par", {"id": sec_id})
        ET.SubElement(par_elem, "text", {"src": f"book.xml#{sec_id}"})
        # Add an empty audio element for compatibility
        ET.SubElement(par_elem, "audio", {"src": ""})
    smil_xml_str = '<?xml version="1.0" encoding="UTF-8"?>\n'
    smil_xml_str += '<!DOCTYPE smil PUBLIC "-//W3C//DTD SMIL 2.0//EN" "http://www.w3.org/2001/SMIL20/Language.dtd">\n'
    smil_xml_str += ET.tostring(smil_elem, encoding="utf-8").decode("utf-8")

    # 6. Create OPF file (package manifest) as book.opf
    unique_id = str(uuid.uuid4())
    opf_elem = ET.Element("package", {
        "xmlns": "http://openebook.org/namespaces/oeb-package/1.2/",
        "unique-identifier": "BookID",
        "version": "1.2"
    })
    metadata = ET.SubElement(opf_elem, "metadata", {"xmlns:dc": "http://purl.org/dc/elements/1.1/"})
    ET.SubElement(metadata, "dc:title").text = title
    ET.SubElement(metadata, "dc:creator").text = creator
    ET.SubElement(metadata, "dc:language").text = language
    ET.SubElement(metadata, "dc:Identifier", {"id": "BookID"}).text = unique_id
    ET.SubElement(metadata, "meta", {"name": "dtb:uid", "content": unique_id})
    ET.SubElement(metadata, "meta", {"name": "dtb:format", "content": "ANSI/NISO Z39.86-2005"})
    manifest = ET.SubElement(opf_elem, "manifest")
    ET.SubElement(manifest, "item", {"id": "dtbook", "href": "book.xml", "media-type": "application/x-dtbook+xml"})
    ET.SubElement(manifest, "item", {"id": "ncx", "href": "book.ncx", "media-type": "application/x-dtbncx+xml"})
    ET.SubElement(manifest, "item", {"id": "smil", "href": "book.smil", "media-type": "application/smil+xml"})
    # Add image items to the manifest
    for img in image_mapping.values():
        ET.SubElement(manifest, "item", {
            "id": img["filename"],
            "href": f"images/{img['filename']}",
            "media-type": img["content_type"]
        })
    spine = ET.SubElement(opf_elem, "spine", {"toc": "ncx"})
    ET.SubElement(spine, "itemref", {"idref": "dtbook"})
    opf_xml_str = '<?xml version="1.0" encoding="UTF-8"?>\n'
    opf_xml_str += ET.tostring(opf_elem, encoding="utf-8").decode("utf-8")

    # 7. Create ZIP package including XML files and images
    # The OPF file is now named "book.opf" for compatibility.
    with zipfile.ZipFile(output_zip_path, 'w') as z:
        z.writestr("book.xml", dtbook_xml_str)
        z.writestr("book.ncx", ncx_xml_str)
        z.writestr("book.smil", smil_xml_str)
        z.writestr("book.opf", opf_xml_str)
        # Write all image files under the images/ folder
        for rel_id, img in image_mapping.items():
            z.writestr(f"images/{img['filename']}", img["data"])
