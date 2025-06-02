"""
Metadata utility functions.

This module provides common metadata manipulation utilities.
"""

import io
from PIL import Image
import piexif


class MetadataUtils:
    """Utility class for metadata operations."""
    
    @staticmethod
    def create_xmp_metadata(title="Test Image with XMP", description="Sample image for XMP metadata testing", 
                           creator="Test Generator", tool="Python Test Image Toolkit"):
        """
        Create basic XMP metadata block.
        
        Args:
            title (str): Image title
            description (str): Image description
            creator (str): Creator name
            tool (str): Creator tool
            
        Returns:
            str: XMP metadata XML string
        """
        return f'''<?xml version="1.0" encoding="UTF-8"?>
<x:xmpmeta xmlns:x="adobe:ns:meta/" x:xmptk="Test Generator 1.0">
 <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about=""
      xmlns:dc="http://purl.org/dc/elements/1.1/"
      xmlns:xmp="http://ns.adobe.com/xap/1.0/">
   <dc:title>
    <rdf:Alt>
     <rdf:li xml:lang="x-default">{title}</rdf:li>
    </rdf:Alt>
   </dc:title>
   <dc:description>
    <rdf:Alt>
     <rdf:li xml:lang="x-default">{description}</rdf:li>
    </rdf:Alt>
   </dc:description>
   <dc:creator>
    <rdf:Seq>
     <rdf:li>{creator}</rdf:li>
    </rdf:Seq>
   </dc:creator>
   <xmp:CreateDate>2025-05-31T12:00:00</xmp:CreateDate>
   <xmp:ModifyDate>2025-05-31T12:00:00</xmp:ModifyDate>
   <xmp:CreatorTool>{tool}</xmp:CreatorTool>
  </rdf:Description>
 </rdf:RDF>
</x:xmpmeta>'''
    
    @staticmethod
    def create_complex_xmp_metadata():
        """
        Create complex XMP metadata with custom namespaces and nested structures.
        
        Returns:
            str: Complex XMP metadata XML string
        """
        return '''<?xml version="1.0" encoding="UTF-8"?>
<x:xmpmeta xmlns:x="adobe:ns:meta/" x:xmptk="Test Generator 1.0">
 <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about=""
      xmlns:dc="http://purl.org/dc/elements/1.1/"
      xmlns:xmp="http://ns.adobe.com/xap/1.0/"
      xmlns:custom="http://example.com/test/1.0/">
   <dc:title>
    <rdf:Alt>
     <rdf:li xml:lang="en">Complex XMP Test</rdf:li>
     <rdf:li xml:lang="ja">複雑なXMPテスト</rdf:li>
    </rdf:Alt>
   </dc:title>
   <dc:subject>
    <rdf:Bag>
     <rdf:li>test</rdf:li>
     <rdf:li>metadata</rdf:li>
     <rdf:li>xmp</rdf:li>
     <rdf:li>complex</rdf:li>
    </rdf:Bag>
   </dc:subject>
   <custom:testProperty>Custom Value</custom:testProperty>
   <custom:nestedStructure>
    <rdf:Description>
     <custom:level1>Value 1</custom:level1>
     <custom:level2>
      <rdf:Description>
       <custom:nested>Deep nested value</custom:nested>
      </rdf:Description>
     </custom:level2>
    </rdf:Description>
   </custom:nestedStructure>
  </rdf:Description>
 </rdf:RDF>
</x:xmpmeta>'''
    
    @staticmethod
    def create_conflicting_xmp_metadata():
        """
        Create XMP metadata for conflict testing.
        
        Returns:
            str: XMP metadata XML string with conflicting data
        """
        return '''<?xml version="1.0" encoding="UTF-8"?>
<x:xmpmeta xmlns:x="adobe:ns:meta/" x:xmptk="Test Generator 1.0">
 <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about=""
      xmlns:dc="http://purl.org/dc/elements/1.1/">
   <dc:title>
    <rdf:Alt>
     <rdf:li xml:lang="x-default">XMP Title</rdf:li>
    </rdf:Alt>
   </dc:title>
   <dc:description>
    <rdf:Alt>
     <rdf:li xml:lang="x-default">XMP Description</rdf:li>
    </rdf:Alt>
   </dc:description>
  </rdf:Description>
 </rdf:RDF>
</x:xmpmeta>'''
    
    @staticmethod
    def get_iptc_commands():
        """
        Get IPTC metadata command parameters for ImageMagick.
        
        Returns:
            list: List of IPTC command parameters
        """
        return [
            "-set", "iptc:2:120", "IPTC Test Caption",
            "-set", "iptc:2:80", "Test Generator",
            "-set", "iptc:2:05", "IPTC Test Title",
            "-set", "iptc:2:25", "iptc metadata test",
            "-set", "iptc:2:110", "Photo credit test",
            "-set", "iptc:2:116", "Copyright Test 2025"
        ]
    
    @staticmethod
    def get_conflicting_iptc_commands():
        """
        Get conflicting IPTC metadata command parameters for ImageMagick.
        
        Returns:
            list: List of conflicting IPTC command parameters
        """
        return [
            "-set", "iptc:2:05", "IPTC Title (Different)",
            "-set", "iptc:2:120", "IPTC Caption (Different)"
        ]
    
    @staticmethod
    def create_exif_thumbnail(source_image, thumbnail_size=(160, 120)):
        """
        Create EXIF thumbnail data from source image.
        
        Args:
            source_image (PIL.Image): Source image
            thumbnail_size (tuple): Thumbnail size (width, height)
            
        Returns:
            bytes: Thumbnail JPEG data
        """
        # Create thumbnail
        thumbnail = source_image.copy()
        thumbnail.thumbnail(thumbnail_size, Image.Resampling.LANCZOS)
        
        # Convert thumbnail to JPEG bytes
        thumb_buffer = io.BytesIO()
        thumbnail.save(thumb_buffer, format='JPEG', quality=85)
        return thumb_buffer.getvalue()
    
    @staticmethod
    def load_or_create_exif(source_file):
        """
        Load existing EXIF data or create new empty structure.
        
        Args:
            source_file (str): Path to source image file
            
        Returns:
            dict: EXIF data structure
        """
        try:
            return piexif.load(str(source_file))
        except:
            return {"0th": {}, "Exif": {}, "GPS": {}, "1st": {}, "thumbnail": None}
    
    @staticmethod
    def set_orientation(exif_data, orientation):
        """
        Set EXIF orientation tag.
        
        Args:
            exif_data (dict): EXIF data structure
            orientation (int): Orientation value (1-8)
        """
        exif_data["0th"][piexif.ImageIFD.Orientation] = orientation
    
    @staticmethod
    def set_dpi_exif(exif_data, dpi, units=2):
        """
        Set DPI in EXIF data.
        
        Args:
            exif_data (dict): EXIF data structure
            dpi (int): DPI value
            units (int): Resolution unit (2=inches, 3=cm)
        """
        exif_data["0th"][piexif.ImageIFD.XResolution] = (dpi, 1)
        exif_data["0th"][piexif.ImageIFD.YResolution] = (dpi, 1)
        exif_data["0th"][piexif.ImageIFD.ResolutionUnit] = units
    
    @staticmethod
    def remove_dpi_exif(exif_data):
        """
        Remove DPI information from EXIF data.
        
        Args:
            exif_data (dict): EXIF data structure
        """
        exif_data["0th"].pop(piexif.ImageIFD.XResolution, None)
        exif_data["0th"].pop(piexif.ImageIFD.YResolution, None)
        exif_data["0th"].pop(piexif.ImageIFD.ResolutionUnit, None)