# worm
Light weight distributed computing for ipython

# Installation
git clone https://github.com/mtconley/worm.git
cd worm
python setup.py install

# Example

##Worm Example

####Make Dummy Data


    import pandas as pd
    import numpy as np
    length = 1000000
    width = length / 5
    dummy = np.random.randint(0, 10, length).reshape((width, 5))
    df = pd.DataFrame(dummy, columns=list('abcde'))

####Create Collection


    import worm


    data = worm.Collection(df)


    data




    [Record({'a': 9, 'c': 9, 'b': 6, 'e': 2, 'd': 6, 'index_record': 0}),
    Record({'a': 8, 'c': 3, 'b': 6, 'e': 1, 'd': 9, 'index_record': 1}),
    Record({'a': 3, 'c': 0, 'b': 4, 'e': 8, 'd': 2, 'index_record': 2}),
    Record({'a': 7, 'c': 8, 'b': 7, 'e': 3, 'd': 7, 'index_record': 3}),
    Record({'a': 0, 'c': 8, 'b': 8, 'e': 8, 'd': 6, 'index_record': 4}),
    ...]
    
    Collection Object with
    200000 Record Objects



####Define Functions


    def square(record):
        record.a = record.a ** 2
        return record
    
    def cube(record):
        record.b = record.b ** 3
        return record




    data.map(mapper).collect()


<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>name</th>
      <th>progress</th>
      <th>update</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>PoolWorker-5</td>
      <td>100.00%</td>
      <td><progress value="100.00" max="100"></progress></td>
    </tr>
    <tr>
      <th>1</th>
      <td>PoolWorker-6</td>
      <td>100.00%</td>
      <td><progress value="100.00" max="100"></progress></td>
    </tr>
    <tr>
      <th>2</th>
      <td>PoolWorker-7</td>
      <td>100.00%</td>
      <td><progress value="100.00" max="100"></progress></td>
    </tr>
    <tr>
      <th>3</th>
      <td>PoolWorker-8</td>
      <td>100.00%</td>
      <td><progress value="100.00" max="100"></progress></td>
    </tr>
  </tbody>
</table>



    data.query(query)


    data




    [Record({'a': 6561, 'c': 9, 'b': 6, 'e': 2, 'd': 6, 'index_record': 0}),
    Record({'a': 4096, 'c': 3, 'b': 6, 'e': 1, 'd': 9, 'index_record': 1}),
    Record({'a': 81, 'c': 0, 'b': 4, 'e': 8, 'd': 2, 'index_record': 2}),
    Record({'a': 2401, 'c': 8, 'b': 7, 'e': 3, 'd': 7, 'index_record': 3}),
    Record({'a': 0, 'c': 8, 'b': 8, 'e': 8, 'd': 6, 'index_record': 4}),
    ...]
    
    Collection Object with
    200000 Record Objects




    data = worm.run(data, query, mappers=[func1, func2, fun3])


    

