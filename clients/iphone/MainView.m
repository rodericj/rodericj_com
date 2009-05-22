#import "MainView.h"
#import "Register.h"
@implementation MainView
-(void)awakeFromNib{
	if(FALSE){
		[self addSubview:loggedInView];
	}
	else{
		[self addSubview:loggedOutView];
	}
}

-(IBOutlet)switchToRegisterView{
	NSLog(@"in switchToRegisterView of main");
	[loggedOutView removeFromSuperview];
	[self addSubview:registerView];
}

@end
