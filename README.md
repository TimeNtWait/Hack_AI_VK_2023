<div id="head" align="left">
  <p>
    <img align="left" src="https://hacks-ai.ru/img/svg/headerBlock-img-1.svg" width="90" height="90">
    <img align="left" src="https://corp.vkcdn.ru/media/images/color_color-5_9gh7nsf_kFXZCcm.png" width="80" height="80"><br><br>
  </p>
  <h1 align="center"><br>Предсказание интенсивности взаимодействия между друзьями в социальной сети ВКонтакте</h1>
</div>

<div id="badges">
  <p align="center">
    <img src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54">
    <img src="https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white">
    <img src="https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white">
    <img src="https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white">
    <img src="https://img.shields.io/badge/jupyter-%23FA0F00.svg?style=for-the-badge&logo=jupyter&logoColor=white">
    <img src="https://img.shields.io/badge/Matplotlib-%230C55A5.svg?style=for-the-badge&logo=Matplotlib&logoColor=white">
    <img src="https://img.shields.io/badge/PyTorch-%23EE4C2C.svg?style=for-the-badge&logo=PyTorch&logoColor=white">
  </p>
</div>

<div id="1.body" align="left">
  <h3>Краткое описание задачи:</h3>
  <p>Участникам хакатона предлагается предсказать интенсивность взаимодействия между пользователями, основываясь на информации об интенсивности других связей и пользовательской информации.</p>
  <h3>Подход</h3>
  <p>Проведен разведывательный анализ данных (EDA) по признакам эго графов каждого пользователя и дополнительной атрибутивной информации, характеризующей как граф пользователя, так и вершины в его графовом пространстве.</p>
  <p>Комбинации вершин u и v - характеризуют разнонаправленные ребра внутри неориентированного эго графа, при этом заметили корреляцию между признаками х1 и х2 и предположили, что каждый из этих признаков характеризует 
    интенсивность взаимодействия вершин графа u и v в разных направлениях.</p>
  <p><b><i>Информация подаваемая на вход модели:</i></b></p>
</div>

![](./media_files/scheme.png)
  
  <p>По атрибутам добавили новых признаков по частоте встречаемости городов, названий университетов и остальных признаков. Задачу решили свести к регрессии, т.е. формирование таблицы с признаками (свойства графа, вершин и ребер), 
    а в качестве целевого таргета выбрана переменная X1</p>
  
  <h3>EDA</h3>
<p>Визуализация эго графа пользователя (ego_id = 8)</p>

![](./media_files/ego_graph_8.jpg)

  
<p>Визуализация эго графа пользователя (ego_id = 120)</p>

![](./media_files/graph_test1_word2vec.png)

График важных признаков

![](./media_files/feature_importance.jpg)

  <h3>Модели</h3>
  <p>В качестве модели применяется CatBoost</p>
  
![](./media_files/logo_catboost.png)
  
  <p>
    <img src="/media_files/logo_catboost.png">
    <ul>
      <li>Бустинговые модели как правило быстрее и лучше работают с табличными данными</li>
      <li>Прост в развертывании и использовании в отличие от нейронных сетей</li>
      <li>Использует небрежные деревья решений, чтобы вырастить сбалансированное дерево</li>
      <li>Позволяет получить неплохие результаты с параметрами по умолчанию, что сокращает время, необходимое для настройки гиперпараметров</li>
    </ul>
  </p>
  
  <h3>Результаты</h3>
  <p>По графику функции потерь RMSE видно что модель неплохо обучается и может давать предсказания с низкой погрешностью. За счет настройки гиперпараметров удалось снизить ошибку модели RMSE с 1,2 до 0,78</p>
 
![](./media_files/loss_catboost.jpg)

<p>Выгрузка submitions и тестирование в системе</p>

![](./media_files/submission_results.png)
![](./media_files/result_sub_3.jpg)
  
  <h3>Что можно улучшить?</h3>
  <p>
    <ul>
      <li>Добавить графовые модели для формирования эмбеддинга графа, реализованные с учетом методов Deep Walk по случайным блужданиям</li>
      <li>Обрабатывать данные с помощью pyspark, чтобы захватить полный объем датасетов</li>
      <li>Применить фич инжиниринг, для формирования новых признаков</li>
      <li>Реализовать ансамбль моделей</li>
    </ul>
  </p>

Miro решения: https://miro.com/app/board/uXjVMJQAtKM=/ 
