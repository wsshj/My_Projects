#include "leftwidget.h"
#include "ui_leftwidget.h"

LeftWidget::LeftWidget(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::LeftWidget)
{
    ui->setupUi(this);

    m_pal.setColor(QPalette::Background, Qt::yellow);
    setAutoFillBackground(true);
    setPalette(m_pal);

    m_button = new QPushButton(this);
    m_button->setText("按钮A");

    connect(m_button,SIGNAL(clicked()),this,SLOT(on_Button_clicked()));
    connect(parent,SIGNAL(sendColor(QColor)),this,SLOT(recvColor(QColor)));
}

LeftWidget::~LeftWidget()
{
    delete ui;
}

void LeftWidget::resizeEvent(QResizeEvent *event)
{
    m_button->setGeometry(width()/2-25,height()/2-15,50,30);
}

void LeftWidget::on_Button_clicked()
{
    emit sendText(m_button->text());
    emit sendColor(Qt::green);
    m_pal.setColor(QPalette::Background, Qt::yellow);
    setPalette(m_pal);
}

void LeftWidget::recvColor(QColor color)
{
    m_pal.setColor(QPalette::Background, color);
    setPalette(m_pal);
}
