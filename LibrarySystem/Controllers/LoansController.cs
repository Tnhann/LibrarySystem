using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using LibrarySystem.Models;
using LibrarySystem.Data;
using System;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc.Rendering;

namespace LibrarySystem.Controllers
{
    public class LoansController : Controller
    {
        private readonly ApplicationDbContext _context;

        public LoansController(ApplicationDbContext context)
        {
            _context = context;
        }

        private bool IsLoggedIn()
        {
            return HttpContext.Session.GetString("IsLoggedIn") == "true";
        }

        // Ödünç alma listesi
        public async Task<IActionResult> Index()
        {
            if (!IsLoggedIn()) return RedirectToAction("Login", "Account");

            var loans = await _context.Loans
                .Include(l => l.Book)
                .Where(l => !l.ReturnDate.HasValue) // Sadece iade edilmemiş kitapları göster
                .OrderByDescending(l => l.LoanDate)
                .ToListAsync();

            return View(loans);
        }

        // Yeni ödünç alma
        public IActionResult Create()
        {
            if (!IsLoggedIn()) return RedirectToAction("Login", "Account");

            ViewBag.Books = new SelectList(
                _context.Books
                    .Where(b => b.Available)
                    .Select(b => new { b.BookID, Title = $"{b.Title} ({b.Author})" }),
                "BookID",
                "Title"
            );

            return View();
        }

        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> Create([Bind("BookID,LoanDate,DueDate")] Loan loan)
        {
            if (!IsLoggedIn()) return RedirectToAction("Login", "Account");

            if (ModelState.IsValid)
            {
                var book = await _context.Books.FindAsync(loan.BookID);
                if (book != null && book.Available)
                {
                    loan.LoanDate = DateTime.Now;
                    loan.MemberID = 1; // Varsayılan üye ID'si
                    book.Available = false;

                    _context.Add(loan);
                    await _context.SaveChangesAsync();
                    TempData["Success"] = "Kitap başarıyla ödünç verildi.";
                    return RedirectToAction(nameof(Index));
                }
            }

            ViewBag.Books = new SelectList(
                _context.Books.Where(b => b.Available),
                "BookID",
                "Title"
            );
            return View(loan);
        }

        // Kitap iadesi
        public async Task<IActionResult> Return(int? id)
        {
            if (!IsLoggedIn()) return RedirectToAction("Login", "Account");

            if (id == null) return NotFound();

            var loan = await _context.Loans
                .Include(l => l.Book)
                .Include(l => l.Member)
                .FirstOrDefaultAsync(l => l.LoanID == id);

            if (loan == null) return NotFound();

            return View(loan);
        }

        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> ReturnConfirmed(int id)
        {
            if (!IsLoggedIn()) return RedirectToAction("Login", "Account");

            var loan = await _context.Loans
                .Include(l => l.Book)
                .FirstOrDefaultAsync(l => l.LoanID == id && !l.ReturnDate.HasValue); // Sadece iade edilmemiş olanları al

            if (loan != null && loan.Book != null)
            {
                loan.ReturnDate = DateTime.Now;
                loan.Book.Available = true; // Kitabı müsait yap

                await _context.SaveChangesAsync();
                TempData["Success"] = "Kitap başarıyla iade edildi.";
            }

            return RedirectToAction(nameof(Index));
        }
    }
} 