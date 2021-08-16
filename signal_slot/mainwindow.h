#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QPushButton>
#include <QLabel>
#include <QStack>

#include "rightwidget.h"
#include "leftwidget.h"

QT_BEGIN_NAMESPACE
namespace Ui { class MainWindow; }
QT_END_NAMESPACE

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

    void init();
    void resizeEvent(QResizeEvent *event) override;
    void lalal();

private:
    Ui::MainWindow *ui;

    RightWidget* m_right;
    LeftWidget* m_left;

    QLabel* m_label;

    QStack<QPushButton*> buttons;


signals:
    void sendColor(QColor color);

private slots:
    void recvText(QString str);
};
#endif // MAINWINDOW_H
