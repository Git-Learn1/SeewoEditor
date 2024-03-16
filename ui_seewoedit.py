from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton

class SEMain(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("希沃启动图片一键替换")
        self.setFixedSize(640, 480)
        self.setCentralWidget(QWidget())
        
        layout = QVBoxLayout()
        
        layout_user_path = QHBoxLayout()
        self.label_user_path = QLabel("未能成功获取用户位置，请手动选择")
        layout_user_path.addWidget(self.label_user_path)
        self.btn_user_path = QPushButton("选择用户图片位置")
        layout_user_path.addWidget(self.btn_user_path)
        layout.addLayout(layout_user_path)
        
        layout_path = QHBoxLayout()
        self.label_path = QLabel("未能成功获取希沃图片位置，请手动选择")
        layout_path.addWidget(self.label_path)
        self.btn_path = QPushButton("选择系统图片位置")
        layout_path.addWidget(self.btn_path)
        layout.addLayout(layout_path)

        layout_seewo_path = QHBoxLayout()
        self.label_seewo_path = QLabel("未能成功获取希沃程序位置，请手动选择")
        layout_seewo_path.addWidget(self.label_seewo_path)
        self.btn_seewo_path = QPushButton("选择希沃程序位置")
        layout_seewo_path.addWidget(self.btn_seewo_path)
        layout.addLayout(layout_seewo_path)

        layout_music_path = QHBoxLayout()
        self.label_music_path = QLabel("（可选）自定义音乐")
        layout_music_path.addWidget(self.label_music_path)
        self.btn_music_path = QPushButton("选择启动音乐位置")
        layout_music_path.addWidget(self.btn_music_path)
        layout.addLayout(layout_music_path)
        
        layout_img = QHBoxLayout()
        self.btn_choose = QPushButton("选择要替换的图片")
        layout_img.addWidget(self.btn_choose)
        self.btn_use_default = QPushButton("使用内置图片")
        layout_img.addWidget(self.btn_use_default)
        layout.addLayout(layout_img)
        
        self.label_img = QLabel("图片预览")
        self.label_img.setScaledContents(True)
        layout.addWidget(self.label_img)
        
        self.btn_replace = QPushButton("开始替换")
        layout.addWidget(self.btn_replace)
        
        self.btn_lnk = QPushButton("替换快捷方式")
        layout.addWidget(self.btn_lnk)

        self.btn_fix = QPushButton("一键还原所有操作")
        layout.addWidget(self.btn_fix)
        
        self.btn_start = QPushButton("希沃，启动！")
        layout.addWidget(self.btn_start)
        
        self.centralWidget().setLayout(layout)
            