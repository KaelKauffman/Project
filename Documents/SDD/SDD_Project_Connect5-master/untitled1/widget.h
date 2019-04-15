#ifndef WIDGET_H
#define WIDGET_H

#include <QWidget>

namespace Ui {
class Widget;
}

class Widget : public QWidget
{
    Q_OBJECT

public:
    explicit Widget(QWidget *parent = nullptr);
    ~Widget();

private slots:
    void on_UserButton_clicked();

    void on_GameRecommendationButton_clicked();

    void on_SteamRushText_clicked();

    void on_PriceCheckButton_clicked();

    void on_LoginButton_clicked();


    void on_RankingButton_clicked();

private:
    Ui::Widget *ui;
};

#endif // WIDGET_H
