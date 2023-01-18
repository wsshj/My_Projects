#include "mainwindow.h"
#include "ui_mainwindow.h"

#include <QFile>
#include <QJsonDocument>
#include <QJsonObject>
#include <QDebug>
#include <QJsonArray>

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);

    init();
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::init()
{
    m_right = new RightWidget(this);
    m_left = new LeftWidget(this);

    m_label = new QLabel(this);

    m_label->setText("hello world");
    m_label->setAlignment(Qt::AlignCenter);

    connect(m_left,SIGNAL(sendText(QString)),this,SLOT(recvText(QString)));
    connect(m_right,SIGNAL(sendText(QString)),this,SLOT(recvText(QString)));

    connect(m_left,SIGNAL(sendColor(QColor)),this,SIGNAL(sendColor(QColor)));
    connect(m_right,SIGNAL(sendColor(QColor)),this,SIGNAL(sendColor(QColor)));
}

void MainWindow::resizeEvent(QResizeEvent *event)
{
    m_left->setGeometry(0,100,width()/2-2,height());
    m_right->setGeometry(width()/2+2,100,width()/2-2,height());

    m_label->setGeometry(width()/2-75,30,150,30);
}

void MainWindow::recvText(QString str)
{
    m_label->setText(str);
}

