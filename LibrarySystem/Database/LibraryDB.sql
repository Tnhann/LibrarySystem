USE master;
GO

-- Eğer veritabanı varsa sil
IF EXISTS (SELECT * FROM sys.databases WHERE name = 'LibraryDB')
BEGIN
    ALTER DATABASE LibraryDB SET SINGLE_USER WITH ROLLBACK IMMEDIATE;
    DROP DATABASE LibraryDB;
END
GO

-- Yeni veritabanı oluştur
CREATE DATABASE LibraryDB;
GO

USE LibraryDB;
GO

-- Kategoriler tablosu
CREATE TABLE Categories (
    CategoryID INT PRIMARY KEY IDENTITY(1,1),
    CategoryName NVARCHAR(50) NOT NULL
);

-- Kitaplar tablosu
CREATE TABLE Books (
    BookID INT PRIMARY KEY IDENTITY(1,1),
    ISBN VARCHAR(13),
    Title NVARCHAR(100) NOT NULL,
    Author NVARCHAR(100) NOT NULL,
    PublishYear INT,
    Publisher NVARCHAR(100),
    Available BIT DEFAULT 1,
    CategoryID INT NOT NULL,
    FOREIGN KEY (CategoryID) REFERENCES Categories(CategoryID)
);

-- Üyeler tablosu
CREATE TABLE Members (
    MemberID INT PRIMARY KEY IDENTITY(1,1),
    FirstName NVARCHAR(50) NOT NULL,
    LastName NVARCHAR(50) NOT NULL,
    Email NVARCHAR(100) NOT NULL UNIQUE,
    Phone VARCHAR(15),
    RegistrationDate DATETIME DEFAULT GETDATE()
);

-- Kullanıcılar tablosu
CREATE TABLE Users (
    UserID INT PRIMARY KEY IDENTITY(1,1),
    Username NVARCHAR(50) NOT NULL UNIQUE,
    Password NVARCHAR(100) NOT NULL,
    Email NVARCHAR(100) UNIQUE,
    Role NVARCHAR(20) NOT NULL DEFAULT 'User',
    CreatedDate DATETIME DEFAULT GETDATE()
);

-- Ödünç alma işlemleri tablosu
CREATE TABLE Loans (
    LoanID INT PRIMARY KEY IDENTITY(1,1),
    BookID INT NOT NULL,
    MemberID INT NOT NULL,
    LoanDate DATETIME DEFAULT GETDATE(),
    DueDate DATETIME NOT NULL,
    ReturnDate DATETIME,
    FOREIGN KEY (BookID) REFERENCES Books(BookID),
    FOREIGN KEY (MemberID) REFERENCES Members(MemberID)
);

-- Örnek verileri ekle
INSERT INTO Categories (CategoryName) VALUES 
('Roman'),
('Bilim'),
('Tarih'),
('Felsefe'),
('Çocuk Kitapları');

-- Admin kullanıcısı ekleme
INSERT INTO Users (Username, Password, Email, Role, CreatedDate) VALUES 
('admin', 'admin123', 'admin@library.com', 'Admin', GETDATE()),
('user1', 'user123', 'user1@library.com', 'User', GETDATE()),
('librarian', 'lib123', 'librarian@library.com', 'Librarian', GETDATE());

INSERT INTO Books (Title, Author, ISBN, PublishYear, Publisher, CategoryID, Available) VALUES
('Suç ve Ceza', 'Fyodor Dostoyevski', '9789750719387', 1866, 'İş Bankası Yayınları', 1, 1),
('1984', 'George Orwell', '9789750718518', 1949, 'Can Yayınları', 1, 1),
('Evrenin Kısa Tarihi', 'Stephen Hawking', '9786053757818', 1988, 'Alfa Yayınları', 2, 1),
('Nutuk', 'Mustafa Kemal Atatürk', '9789751614109', 1927, 'Türk Tarih Kurumu', 3, 1),
('Sofienin Dünyası', 'Jostein Gaarder', '9789750726477', 1991, 'Pan Yayıncılık', 4, 1),
('Küçük Prens', 'Antoine de Saint-Exupéry', '9789750726477', 1943, 'Can Çocuk', 5, 1);

INSERT INTO Members (FirstName, LastName, Email, Phone) VALUES
('Ahmet', 'Yılmaz', 'ahmet@example.com', '5551234567'),
('Ayşe', 'Kaya', 'ayse@example.com', '5559876543'),
('Mehmet', 'Demir', 'mehmet@example.com', '5553334444'); 