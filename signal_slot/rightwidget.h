#ifndef RIGHTWIDGET_H
#define RIGHTWIDGET_H

#include <QWidget>
#include <QPalette>
#include <QPushButton>
#include <QLabel>

namespace Ui {
class RightWidget;
}

class RightWidget : public QWidget
{
    Q_OBJECT

public:
    explicit RightWidget(QWidget *parent = nullptr);
    ~RightWidget();

    void resizeEvent(QResizeEvent *event) override;

private:
    Ui::RightWidget *ui;

    QPalette m_pal;

    QPushButton* m_button;
    QLabel* m_label;

signals:
    void sendText(QString str);
    void sendColor(QColor color);

//声明槽
private slots:
    void on_Button_clicked();
    void recvColor(QColor color);
};

#endif // RIGHTWIDGET_H
