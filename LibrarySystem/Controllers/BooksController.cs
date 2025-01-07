using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using LibrarySystem.Models;
using LibrarySystem.Data;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc.Rendering;
using System;

namespace LibrarySystem.Controllers
{
    public class BooksController : Controller
    {
        private readonly ApplicationDbContext _context;

        public BooksController(ApplicationDbContext context)
        {
            _context = context;
        }

        private bool IsLoggedIn()
        {
            return HttpContext.Session.GetString("IsLoggedIn") == "true";
        }

        // GET: Books
        public async Task<IActionResult> Index(string searchString, int? categoryId, bool? availability)
        {
            if (!IsLoggedIn()) return RedirectToAction("Login", "Account");

            try
            {
                // Kategorileri ViewBag'e ekle
                ViewBag.Categories = await _context.Categories.ToListAsync();

                // Sorguyu oluştur
                var query = _context.Books.AsQueryable();

                // Kategori ilişkisini ekle
                query = query.Include(b => b.Category);

                // Arama filtresi
                if (!string.IsNullOrEmpty(searchString))
                {
                    searchString = searchString.ToLower();
                    query = query.Where(b => 
                        b.Title.ToLower().Contains(searchString) ||
                        b.Author.ToLower().Contains(searchString) ||
                        (b.ISBN != null && b.ISBN.Contains(searchString)));
                }

                // Kategori filtresi
                if (categoryId.HasValue)
                {
                    query = query.Where(b => b.CategoryID == categoryId);
                }

                // Durum filtresi
                if (availability.HasValue)
                {
                    query = query.Where(b => b.Available == availability);
                }

                // Sonuçları getir
                var books = await query.ToListAsync();

                // ViewData'yı ayarla
                ViewData["CurrentFilter"] = searchString;
                ViewData["CurrentCategory"] = categoryId;
                ViewData["CurrentAvailability"] = availability;

                return View(books);
            }
            catch (Exception ex)
            {
                TempData["Error"] = "Kitaplar listelenirken bir hata oluştu: " + ex.Message;
                return View(new List<Book>());
            }
        }

        public async Task<IActionResult> Details(int? id)
        {
            if (id == null)
            {
                return NotFound();
            }

            var book = await _context.Books
                .Include(b => b.Category)
                .FirstOrDefaultAsync(m => m.BookID == id);

            if (book == null)
            {
                return NotFound();
            }

            return View(book);
        }

        // CREATE
        public IActionResult Create()
        {
            if (!IsLoggedIn())
            {
                return RedirectToAction("Login", "Account");
            }

            ViewBag.Categories = new SelectList(_context.Categories, "CategoryID", "CategoryName");
            return View();
        }

        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> Create([Bind("Title,Author,ISBN,PublishYear,Publisher,CategoryID")] Book book)
        {
            if (!IsLoggedIn())
            {
                return RedirectToAction("Login", "Account");
            }

            try
            {
                book.Available = true;
                _context.Books.Add(book);
                await _context.SaveChangesAsync();

                TempData["Success"] = $"Kitap başarıyla eklendi! Başlık: {book.Title}, Yazar: {book.Author}";
                
                await _context.SaveChangesAsync();
                
                return RedirectToAction(nameof(Index));
            }
            catch (Exception ex)
            {
                ModelState.AddModelError("", $"Kitap eklenirken bir hata oluştu: {ex.Message}");
                TempData["Error"] = $"Kitap eklenemedi: {ex.Message}";
            }

            ViewBag.Categories = new SelectList(_context.Categories, "CategoryID", "CategoryName", book.CategoryID);
            return View(book);
        }

        // EDIT
        public async Task<IActionResult> Edit(int? id)
        {
            if (!IsLoggedIn())
            {
                return RedirectToAction("Login", "Account");
            }

            if (id == null)
            {
                return NotFound();
            }

            var book = await _context.Books.FindAsync(id);
            if (book == null)
            {
                return NotFound();
            }

            ViewBag.Categories = new SelectList(_context.Categories, "CategoryID", "CategoryName", book.CategoryID);
            return View(book);
        }

        [HttpPost]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> Edit(int id, [Bind("BookID,Title,Author,ISBN,PublishYear,Publisher,CategoryID,Available")] Book book)
        {
            if (!IsLoggedIn()) return RedirectToAction("Login", "Account");

            if (id != book.BookID) return NotFound();

            try
            {
                var existingBook = await _context.Books
                    .Include(b => b.Loans)
                    .FirstOrDefaultAsync(b => b.BookID == id);

                if (existingBook == null) return NotFound();

                // Kitap bilgilerini güncelle
                existingBook.Title = book.Title;
                existingBook.Author = book.Author;
                existingBook.ISBN = book.ISBN;
                existingBook.PublishYear = book.PublishYear;
                existingBook.Publisher = book.Publisher;
                existingBook.CategoryID = book.CategoryID;

                // Eğer Available değeri değiştiyse ve true yapıldıysa
                if (book.Available && !existingBook.Available)
                {
                    // Aktif ödünç kayıtlarını kapat
                    var activeLoans = await _context.Loans
                        .Where(l => l.BookID == id && !l.ReturnDate.HasValue)
                        .ToListAsync();

                    foreach (var loan in activeLoans)
                    {
                        loan.ReturnDate = DateTime.Now;
                    }
                }

                existingBook.Available = book.Available;
                await _context.SaveChangesAsync();
                
                TempData["Success"] = $"'{book.Title}' başarıyla güncellendi!";
                return RedirectToAction(nameof(Index));
            }
            catch (DbUpdateConcurrencyException)
            {
                if (!BookExists(book.BookID))
                {
                    return NotFound();
                }
                else
                {
                    ModelState.AddModelError("", "Güncelleme sırasında bir hata oluştu. Lütfen tekrar deneyin.");
                    TempData["Error"] = "Kitap güncellenemedi!";
                }
            }

            ViewBag.Categories = new SelectList(_context.Categories, "CategoryID", "CategoryName", book.CategoryID);
            return View(book);
        }

        // DELETE
        public async Task<IActionResult> Delete(int? id)
        {
            if (!IsLoggedIn()) return RedirectToAction("Login", "Account");
            
            if (id == null) return NotFound();

            var book = await _context.Books
                .Include(b => b.Category)
                .Include(b => b.Loans)
                .FirstOrDefaultAsync(m => m.BookID == id);

            if (book == null) return NotFound();

            // Eğer kitap ödünç verilmişse silmeye izin verme
            if (!book.Available || book.Loans.Any(l => !l.ReturnDate.HasValue))
            {
                TempData["Error"] = "Ödünç verilmiş kitap silinemez!";
                return RedirectToAction(nameof(Index));
            }

            return View(book);
        }

        [HttpPost, ActionName("Delete")]
        [ValidateAntiForgeryToken]
        public async Task<IActionResult> DeleteConfirmed(int id)
        {
            if (!IsLoggedIn()) return RedirectToAction("Login", "Account");

            var book = await _context.Books
                .Include(b => b.Loans)
                .FirstOrDefaultAsync(b => b.BookID == id);

            if (book == null) return NotFound();

            // Son bir kontrol daha yap
            if (!book.Available || book.Loans.Any(l => !l.ReturnDate.HasValue))
            {
                TempData["Error"] = "Ödünç verilmiş kitap silinemez!";
                return RedirectToAction(nameof(Index));
            }

            _context.Books.Remove(book);
            await _context.SaveChangesAsync();
            TempData["Success"] = "Kitap başarıyla silindi.";
            
            return RedirectToAction(nameof(Index));
        }

        private bool BookExists(int id)
        {
            return _context.Books.Any(e => e.BookID == id);
        }

        public IActionResult Image(int id)
        {
            var book = _context.Books.Find(id);
            if (book == null)
            {
                return NotFound();
            }
            
            // Örnek bir resim döndür
            return File("~/images/book-placeholder.jpg", "image/jpeg");
        }
    }
} 