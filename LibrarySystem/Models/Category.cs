using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;

namespace LibrarySystem.Models
{
    public class Category
    {
        [Key]
        public int CategoryID { get; set; }
        
        [Required]
        [StringLength(50)]
        public string CategoryName { get; set; }
        
        public virtual ICollection<Book> Books { get; set; }
    }
} 