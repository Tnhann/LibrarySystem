using System;
using System.ComponentModel.DataAnnotations;

namespace LibrarySystem.Models
{
    public class User
    {
        public int UserID { get; set; }
        
        [Required]
        [StringLength(50)]
        public string Username { get; set; }
        
        [Required]
        [StringLength(100)]
        public string Password { get; set; }
        
        [EmailAddress]
        public string Email { get; set; }
        
        public string Role { get; set; }
        
        public DateTime CreatedDate { get; set; }
    }
} 