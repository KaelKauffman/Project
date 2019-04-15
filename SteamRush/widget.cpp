#include "widget.h"
#include "ui_widget.h"

Widget::Widget(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::Widget)
{
    ui->setupUi(this);
}

Widget::~Widget()
{
    delete ui;
}

void Widget::on_SteamRushText_clicked()
{
    //Bring back to home page.
    ui->Pages->setCurrentIndex(0);
}

void Widget::on_UserButton_clicked()
{
    //Bring to User page.
    ui->Pages->setCurrentIndex(2);
}

void Widget::on_GameRecommendationButton_clicked()
{
    //Bring to Game Rec page.
    ui->Pages->setCurrentIndex(3);
}

void Widget::on_PriceCheckButton_clicked()
{
    ui->Pages->setCurrentIndex(4);
}

void Widget::on_LoginButton_clicked()
{
    //Bring to Log In page.
    ui->Pages->setCurrentIndex(5);
}




void Widget::on_RankingButton_clicked()
{
    ui->Pages->setCurrentIndex(1);
}
