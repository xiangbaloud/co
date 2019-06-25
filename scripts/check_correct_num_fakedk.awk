BEGIN{
count=0;
}
{
	if ($5=="type")
	{
		if (fakedk ==1)
		{
			if ($6==2 || $6==0)
		  	count ++;	
		}
		else
		{
			if ($6==2 )
		  	count ++;	
		}
	}		
}
END{
	print count
}
