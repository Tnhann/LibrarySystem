using Microsoft.AspNetCore.Mvc;
using LibrarySystem.Models;
using LibrarySystem.Data;
using Microsoft.EntityFrameworkCore;

namespace LibrarySystem.Controllers
{
    public class HomeController : Controller
    {
        private readonly ApplicationDbContext _context;

        public HomeController(ApplicationDbContext context)
        {
            _context = context;
        }

        public IActionResult Index()
        {
            if (HttpContext.Session.GetString("IsLoggedIn") == "true")
            {
                ViewBag.TotalBooks = _context.Books.Count();
                ViewBag.AvailableBooks = _context.Books.Count(b => b.Available);
                ViewBag.LoanedBooks = _context.Books.Count(b => !b.Available);
                ViewBag.Categories = _context.Categories.Count();
            }
            return View();
        }

        public IActionResult Error()
        {
            return View();
        }
    }
} 