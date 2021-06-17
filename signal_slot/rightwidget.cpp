#include "rightwidget.h"
#include "ui_rightwidget.h"

RightWidget::RightWidget(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::RightWidget)
{
    ui->setupUi(this);

    m_pal.setColor(QPalette::Background, Qt::red);
    setAutoFillBackground(true);
    setPalette(m_pal);

    m_button = new QPushButton(this);
    m_button->setText("按钮B");

    connect(m_button,SIGNAL(clicked()),this,SLOT(on_Button_clicked()));
    connect(parent,SIGNAL(sendColor(QColor)),this,SLOT(recvColor(QColor)));
}

RightWidget::~RightWidget()
{
    delete ui;
}

void RightWidget::resizeEvent(QResizeEvent *event)
{
    m_button->setGeometry(width()/2-25,height()/2-15,50,30);
}

void RightWidget::on_Button_clicked()
{
    emit sendText(m_button->text());
    emit sendColor(Qt::blue);
    m_pal.setColor(QPalette::Background, Qt::red);
    setPalette(m_pal);
}

void RightWidget::recvColor(QColor color)
{
    m_pal.setColor(QPalette::Background, color);
    setPalette(m_pal);
}
