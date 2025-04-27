import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
    QComboBox, QMessageBox, QAction, QAbstractItemView
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class MovieManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🎬 Movie Manager")
        self.setGeometry(100, 100, 900, 600)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #ECEFF1;
            }
            QPushButton {
                padding: 8px;
                border-radius: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #CFD8DC;
            }
            QTableWidget {
                background-color: white;
                alternate-background-color: #F1F8E9;
            }
        """)
        self.history = []
        self.setupUI()

    def setupUI(self):
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        layout = QVBoxLayout()

        # Judul
        titleLabel = QLabel("🎬 Movie Manager")
        titleLabel.setFont(QFont("Poppins", 26, QFont.Bold))
        titleLabel.setStyleSheet("color: #37474F; margin-bottom: 15px;")
        titleLabel.setAlignment(Qt.AlignCenter)
        layout.addWidget(titleLabel)

        # Input
        formLayout = QHBoxLayout()
        self.titleInput = QLineEdit()
        self.titleInput.setPlaceholderText("Masukkan Judul Film...")
        formLayout.addWidget(self.titleInput)

        self.yearInput = QLineEdit()
        self.yearInput.setPlaceholderText("Tahun Rilis...")
        formLayout.addWidget(self.yearInput)

        self.genreInput = QComboBox()
        self.genreInput.addItems(["Action", "Comedy", "Drama", "Fantasy", "Horror", "Romance", "Sci-Fi", "Thriller"])
        formLayout.addWidget(self.genreInput)

        self.ratingInput = QComboBox()
        self.ratingInput.addItems([str(i) for i in range(1, 11)])  
        formLayout.addWidget(self.ratingInput)

        layout.addLayout(formLayout)

        # Tabel
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["Judul", "Tahun", "Genre", "Rating", "Ditonton", "Favorit"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        layout.addWidget(self.table)

        # Tombol
        buttonLayout = QHBoxLayout()

        self.addButton = QPushButton("➕ Tambah Film")
        self.addButton.setStyleSheet("background-color: #81C784; color: white;")
        self.addButton.clicked.connect(self.addMovie)
        buttonLayout.addWidget(self.addButton)

        self.deleteButton = QPushButton("🗑️ Hapus Film")
        self.deleteButton.setStyleSheet("background-color: #E57373; color: white;")
        self.deleteButton.clicked.connect(self.deleteMovie)
        buttonLayout.addWidget(self.deleteButton)

        self.watchedButton = QPushButton("✅ Tandai Ditonton")
        self.watchedButton.setStyleSheet("background-color: #64B5F6; color: white;")
        self.watchedButton.clicked.connect(self.markAsWatched)
        buttonLayout.addWidget(self.watchedButton)

        self.favoriteButton = QPushButton("⭐ Favoritkan")
        self.favoriteButton.setStyleSheet("background-color: #FFD54F; color: black;")
        self.favoriteButton.clicked.connect(self.markAsFavorite)
        buttonLayout.addWidget(self.favoriteButton)

        layout.addLayout(buttonLayout)

        # Student Info 
        studentInfo = QLabel("F1D02310144 - M. Bayu Aji")
        studentInfo.setFont(QFont("Poppins", 11))
        studentInfo.setStyleSheet("color: #90A4AE; margin-top: 20px; margin-bottom: 10px;")
        studentInfo.setAlignment(Qt.AlignCenter)
        layout.addWidget(studentInfo)

        self.centralWidget.setLayout(layout)

        # Menu Bar
        self.menuBar = self.menuBar()
        fileMenu = self.menuBar.addMenu("File")
        aboutMenu = self.menuBar.addMenu("About")
        historyMenu = self.menuBar.addMenu("History")

        exitAction = QAction("Keluar", self)
        exitAction.triggered.connect(self.close)
        fileMenu.addAction(exitAction)

        aboutAction = QAction("Tentang Aplikasi", self)
        aboutAction.triggered.connect(self.showAbout)
        aboutMenu.addAction(aboutAction)

        showHistoryAction = QAction("Lihat Riwayat", self)
        showHistoryAction.triggered.connect(self.showHistory)
        historyMenu.addAction(showHistoryAction)

    def addMovie(self):
        title = self.titleInput.text()
        year = self.yearInput.text()
        genre = self.genreInput.currentText()
        rating = self.ratingInput.currentText()
        watched = "Belum"
        favorite = "Tidak"

        if title.strip() == "" or year.strip() == "":
            QMessageBox.warning(self, "Peringatan", "Judul dan Tahun film harus diisi!")
            return

        if not year.isdigit():
            QMessageBox.warning(self, "Peringatan", "Tahun harus berupa angka!")
            return

        rowCount = self.table.rowCount()
        self.table.insertRow(rowCount)
        self.table.setItem(rowCount, 0, QTableWidgetItem(title))
        self.table.setItem(rowCount, 1, QTableWidgetItem(year))
        self.table.setItem(rowCount, 2, QTableWidgetItem(genre))
        self.table.setItem(rowCount, 3, QTableWidgetItem(rating))
        self.table.setItem(rowCount, 4, QTableWidgetItem(watched))
        self.table.setItem(rowCount, 5, QTableWidgetItem(favorite))

        self.titleInput.clear()
        self.yearInput.clear()
        self.genreInput.setCurrentIndex(0)
        self.ratingInput.setCurrentIndex(0)

        self.history.append(f"Tambah Film: {title} ({year}, {genre}, Rating: {rating})")

    def deleteMovie(self):
        selectedRow = self.table.currentRow()
        if selectedRow >= 0:
            titleItem = self.table.item(selectedRow, 0)
            confirm = QMessageBox.question(
                self, "Konfirmasi", "Apakah yakin ingin menghapus film ini?",
                QMessageBox.Yes | QMessageBox.No
            )
            if confirm == QMessageBox.Yes:
                self.history.append(f"Hapus Film: {titleItem.text()}")
                self.table.removeRow(selectedRow)
        else:
            QMessageBox.warning(self, "Peringatan", "Pilih baris yang ingin dihapus terlebih dahulu!")

    def markAsWatched(self):
        selectedRow = self.table.currentRow()
        if selectedRow >= 0:
            titleItem = self.table.item(selectedRow, 0)
            self.table.setItem(selectedRow, 4, QTableWidgetItem("Ya"))
            self.history.append(f"Tandai Sudah Ditonton: {titleItem.text()}")
        else:
            QMessageBox.warning(self, "Peringatan", "Pilih film yang ingin ditandai!")

    def markAsFavorite(self):
        selectedRow = self.table.currentRow()
        if selectedRow >= 0:
            titleItem = self.table.item(selectedRow, 0)
            self.table.setItem(selectedRow, 5, QTableWidgetItem("Ya"))
            self.history.append(f"Favoritkan Film: {titleItem.text()}")
        else:
            QMessageBox.warning(self, "Peringatan", "Pilih film yang ingin difavoritkan!")

    def showAbout(self):
        QMessageBox.information(self,  "Tentang Aplikasi",
                                "Movie Manager dibuat oleh M. Bayu Aji\nMini Project Visual Programming (PyQt5) 2024/2025.")

    def showHistory(self):
        if not self.history:
            QMessageBox.information(self, "Riwayat Aktivitas", "Belum ada aktivitas.")
        else:
            history_text = "\n".join(self.history)
            QMessageBox.information(self, "Riwayat Aktivitas", history_text)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MovieManager()
    window.show()
    sys.exit(app.exec_())
