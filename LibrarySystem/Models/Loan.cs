using System;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace LibrarySystem.Models
{
    public class Loan
    {
        [Key]
        public int LoanID { get; set; }

        [Required]
        public int BookID { get; set; }

        [Required]
        public int MemberID { get; set; }

        [Required]
        [Display(Name = "Ödünç Alma Tarihi")]
        public DateTime LoanDate { get; set; } = DateTime.Now;

        [Required]
        [Display(Name = "Teslim Tarihi")]
        public DateTime DueDate { get; set; }

        [Display(Name = "İade Tarihi")]
        public DateTime? ReturnDate { get; set; }

        [ForeignKey("BookID")]
        public virtual Book Book { get; set; }

        [ForeignKey("MemberID")]
        public virtual Member Member { get; set; }

        [NotMapped]
        public bool IsOverdue => !ReturnDate.HasValue && DateTime.Now > DueDate;
    }
} 