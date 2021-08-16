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

    QFile file("D:\\Work_Files\\教课\\ss.json");
    file.open(QIODevice::ReadOnly);
    QByteArray data=file.readAll();
    file.close();
    //使用json文件对象加载字符串
    QJsonDocument doc=QJsonDocument::fromJson(data);
    //判断是否对象
    if(doc.isObject())
    {
        //把json文档转换为json对象
        QJsonObject obj=doc.object();
//        QJsonValue value=obj.value("number");
        QString value=obj.value("number").toString();
        QJsonArray member = obj.value("member").toArray();
        for(int i=0;i<member.count();i++)
        {
            qDebug() << member.at(i).toInt();
        }

//        if(value.isObject())
//        {
//            QJsonObject subobj=value.toObject();
//            //取值
//            QString ip=subobj.value("ip").toString();
//            QString port=subobj.value("port").toString();
//            qDebug()<<ip<<port;
//        }
    }
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

void MainWindow::lalal()
{
    QPushButton* button = new QPushButton(this);
    button->setVisible(true);
    button->setGeometry(0,0,100,100);
    buttons.push_back(button);
}

void MainWindow::recvText(QString str)
{
    m_label->setText(str);
    lalal();
}

