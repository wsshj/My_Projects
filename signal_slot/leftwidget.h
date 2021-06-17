#ifndef LEFTWIDGET_H
#define LEFTWIDGET_H

#include <QWidget>
#include <QPalette>
#include <QPushButton>
#include <QLabel>

namespace Ui {
class LeftWidget;
}

class LeftWidget : public QWidget
{
    Q_OBJECT

public:
    explicit LeftWidget(QWidget *parent = nullptr);
    ~LeftWidget();

    void resizeEvent(QResizeEvent *event) override;

private:
    Ui::LeftWidget *ui;

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

#endif // LEFTWIDGET_H
