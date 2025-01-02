using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using System.Collections.Generic;
using System.Linq;

namespace LibrarySystem.Models
{
    public class Book
    {
        [Key]
        public int BookID { get; set; }
        
        [StringLength(13)]
        public string ISBN { get; set; }
        
        [Required(ErrorMessage = "Kitap adı zorunludur")]
        [StringLength(100)]
        public string Title { get; set; }
        
        [Required(ErrorMessage = "Yazar adı zorunludur")]
        [StringLength(100)]
        public string Author { get; set; }
        
        [Range(1000, 2100, ErrorMessage = "Geçerli bir yayın yılı giriniz")]
        public int? PublishYear { get; set; }
        
        [StringLength(100)]
        public string Publisher { get; set; }
        
        public bool Available { get; set; } = true;
        
        [Required(ErrorMessage = "Kategori seçimi zorunludur")]
        public int CategoryID { get; set; }

        [ForeignKey("CategoryID")]
        public virtual Category Category { get; set; }

        public virtual ICollection<Loan> Loans { get; set; }
    }
} 