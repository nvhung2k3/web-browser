import sys
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow, QToolBar, QStatusBar, QAction, QLineEdit, QPushButton, QVBoxLayout, QWidget, QTabWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView

import requests
from bs4 import BeautifulSoup

class WebBrowser(QMainWindow):
    def __init__(self):
        super().__init__()

        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)

        self.browser = QWebEngineView()
        self.browser.setSizePolicy(self.browser.sizePolicy().Expanding, self.browser.sizePolicy().Expanding)
        self.browser.setUrl(QUrl("https://www.google.com"))

        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Enter URL and press Enter")
        self.url_input.returnPressed.connect(self.load_url)

        self.back_button = QPushButton("Back")
        self.back_button.clicked.connect(self.go_back)

        self.forward_button = QPushButton("Forward")
        self.forward_button.clicked.connect(self.go_forward)

        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.load_url)

        self.new_tab_button = QPushButton("+")
        self.new_tab_button.clicked.connect(self.add_new_tab)

        self.news_button = QPushButton("News")
        self.news_button.clicked.connect(self.load_news)

        self.toolbar = QToolBar()
        self.toolbar.addWidget(self.back_button)
        self.toolbar.addWidget(self.forward_button)
        self.toolbar.addSeparator()
        self.toolbar.addWidget(self.new_tab_button)
        self.toolbar.addWidget(self.url_input)
        self.toolbar.addWidget(self.search_button)
        self.toolbar.addWidget(self.news_button)

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        self.central_widget = QWidget()
        self.central_layout = QVBoxLayout()
        self.central_layout.setContentsMargins(0, 0, 0, 0)
        self.central_layout.addWidget(self.toolbar)
        self.central_layout.addWidget(self.tabs)
        self.central_widget.setLayout(self.central_layout)

        self.setCentralWidget(self.central_widget)

        self.browser.urlChanged.connect(self.update_urlbar)
        self.browser.loadFinished.connect(self.update_title)

        self.setWindowTitle("Web Browser")
        self.setGeometry(100, 100, 1024, 768)

        self.add_new_tab()

    def add_new_tab(self):
        new_browser = QWebEngineView()
        new_browser.setUrl(QUrl("https://www.google.com"))
        new_browser.urlChanged.connect(self.update_urlbar)
        new_browser.loadFinished.connect(self.update_title)

        index = self.tabs.addTab(new_browser, "New Tab")
        self.tabs.setCurrentIndex(index)

    def close_tab(self, index):
        if self.tabs.count() > 1:
            widget = self.tabs.widget(index)
            widget.deleteLater()
            self.tabs.removeTab(index)

    def load_url(self):
        url = self.url_input.text()
        if not url.startswith('http://') and not url.startswith('https://'):
            url = 'http://' + url
        current_tab = self.tabs.currentWidget()
        current_tab.setUrl(QUrl(url))

    def update_urlbar(self, q):
        current_tab = self.tabs.currentWidget()
        self.url_input.setText(q.toString())
        self.url_input.setCursorPosition(0)

    def update_title(self):
        current_tab = self.tabs.currentWidget()
        title = current_tab.page().title()
        index = self.tabs.indexOf(current_tab)
        if index >= 0:
            self.tabs.setTabText(index, title)
        self.setWindowTitle(title)

    def go_back(self):
        current_tab = self.tabs.currentWidget()
        current_tab.back()

    def go_forward(self):
        current_tab = self.tabs.currentWidget()
        current_tab.forward()

    def load_news(self):
        news_url = "https://vnexpress.net"  
        response = requests.get(news_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            news_items = soup.find_all('h3', class_='title_news')  

            html = "<h1>News</h1>"
            for item in news_items[:5]:  
                title = item.text
                link = item.find('a')['href']

                
                img = item.find('img')
                if img:
                    img_src = img['src']
                    html += f'<img src="{img_src}" alt="{title}" />'

                html += f'<h2><a href="{link}">{title}</a></h2>'

            current_tab = self.tabs.currentWidget()
            current_tab.setHtml(html, QUrl(news_url))

def main():
    app = QApplication(sys.argv)
    browser = WebBrowser()
    browser.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
