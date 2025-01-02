using Microsoft.AspNetCore.Mvc;
using LibrarySystem.Models;
using LibrarySystem.Data;
using Microsoft.EntityFrameworkCore;
using System.Threading.Tasks;
using System;
using System.Linq;
using Microsoft.AspNetCore.Http;

namespace LibrarySystem.Controllers
{
    public class AccountController : Controller
    {
        private readonly ApplicationDbContext _context;

        public AccountController(ApplicationDbContext context)
        {
            _context = context;
        }

        public IActionResult Login()
        {
            return View();
        }

        [HttpPost]
        public async Task<IActionResult> Login(string username, string password)
        {
            try
            {
                var user = await _context.Users
                    .FirstOrDefaultAsync(u => u.Username == username && u.Password == password);

                if (user != null)
                {
                    HttpContext.Session.SetString("IsLoggedIn", "true");
                    HttpContext.Session.SetString("Username", user.Username);
                    
                    TempData["Message"] = "Hoş geldiniz, " + user.Username + "!";
                    return RedirectToAction("Index", "Home");
                }

                // Hata ayıklama için
                var allUsers = await _context.Users.ToListAsync();
                if (!allUsers.Any())
                {
                    ModelState.AddModelError("", "Veritabanında hiç kullanıcı yok!");
                }
                else
                {
                    ModelState.AddModelError("", "Kullanıcı adı veya şifre hatalı!");
                }
            }
            catch (Exception ex)
            {
                ModelState.AddModelError("", "Giriş işlemi sırasında bir hata oluştu: " + ex.Message);
            }

            return View();
        }

        public IActionResult Logout()
        {
            HttpContext.Session.Clear();
            return RedirectToAction("Index", "Home");
        }
    }
} 