### SQLBatis

#### 20210922
- fix the print issue when no records are fetched
- add proxy to get the rowcount and inserted primary key

#### 20200917
- fix the bug that the row.to_dict(), 'list' object is not callable error

#### 20200918
- fix bug #27, #28

#### 20200922
- give the error details when execute transaction

#### 20200925
- fix bug and enhancement #32 #33

#### 20210627
- compatible the metadata changes(remove reflect param when init metadata)
  in sqlalchemy
- convert the RMKeyView object to list to compatible the 1.4+
- solve the pending rollback issue when inner sql execution has the error